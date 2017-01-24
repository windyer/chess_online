from random import Random

from go.logging import class_wrapper

from django.conf import settings

from card.core.poker import PokerCard

from card.lobby.apps.turner.redis import SessionStatus, TurnerStatistics

@class_wrapper
class TurnerSession(object):

    statistics = TurnerStatistics()

    def __init__(self, session_status):
        self._session_status = session_status
        self._ran = Random()
        self._ran.seed()
        self.win_probability = None
        self._init_probalibliy()

    def _init_probalibliy(self):
        if self._session_status.good_luck:
            self.win_probability = self._ran.choice(settings.TURNER.probabilitys.lucky_probs)
            self.logger.info("[user|%s] get lucky_probs [probabilitys|%s] "
                , self._session_status.id, self.win_probability)
            return

        profit_margin = self.statistics.profit_margin
        if profit_margin >= settings.TURNER.profit_margin.high_criteria:
            self.win_probability = self._ran.choice(settings.TURNER.probabilitys.player_win)
        elif profit_margin <= settings.TURNER.profit_margin.low_criteria:
            self.win_probability = self._ran.choice(settings.TURNER.probabilitys.player_lose)
        else:
            key = self._ran.choice(settings.TURNER.probabilitys.keys())
            self.win_probability = self._ran.choice(settings.TURNER.probabilitys[key])
        
        self.logger.info("[user|%s] [probabilitys|%s] [profit_margin|%f] "
                , self._session_status.id, self.win_probability, profit_margin)

    def _select_rank(self, criterion=None):
        if not criterion:
            criterion = (lambda x: True) 
        return [rank for rank in PokerCard.non_joker_ranks() if criterion(rank)]

    def _player_win(self, choice):
        if (choice == settings.TURNER.large and not self.bigger_ranks or
            choice == settings.TURNER.small and not self.smaller_ranks):
            return False
        elif (choice == settings.TURNER.small and not self.bigger_ranks or
            choice == settings.TURNER.large and not self.smaller_ranks):
            return True
        else:
            if self._ran.random() <= self.win_probability[self.current_round]:
                return True
            else:
                return False

    @classmethod
    def load(cls, user_id):
        if SessionStatus.is_exists(user_id):
            session_stautus = SessionStatus.get_status(user_id)
            return TurnerSession(session_stautus)
        else:
            return None

    @classmethod
    def create(cls, user_id, good_luck=False):
        if SessionStatus.is_exists(user_id):
            session_stautus = SessionStatus.get_status(user_id)
            session_stautus.delete()
        
        session_stautus = SessionStatus.create(user_id, good_luck)
        session_stautus.save()
        return TurnerSession(session_stautus)

    @property
    def status(self):
        return self._session_status.status

    @status.setter
    def status(self, val):
        self._session_status.status = val

    @property
    def current_round(self):
        return self._session_status.current_round

    @property
    def first_round(self):
        return (self.current_round == 0)

    @property
    def second_round(self):
        return (self.current_round ==1)

    @property
    def penultima_round(self):
        return (self.current_round == settings.TURNER.max_round - 2)

    @property
    def last_round(self):
        return (self.current_round == settings.TURNER.max_round - 1)

    @property
    def award_currency(self):
        return settings.TURNER.award_currencys[self.current_round]

    @property
    def game_over(self):
        return (self.status == settings.TURNER.status.win or
                self.status == settings.TURNER.status.lose)

    @property
    def bigger_ranks(self):
        ranks = self._select_rank(lambda x:x.val > self._session_status.current_rank
                                and x.val not in self._session_status.exclude_ranks)
        if self.first_round:
            if len(ranks) > 3:
                if PokerCard.ACE in ranks:
                    ranks.remove(PokerCard.ACE)
                if PokerCard.KING in ranks:
                    ranks.remove(PokerCard.KING)
                if PokerCard.QUEENE in ranks:
                    ranks.remove(PokerCard.QUEENE)
        elif self.second_round:
            if len(ranks) > 2:
                if PokerCard.ACE in ranks:
                    ranks.remove(PokerCard.ACE)
                if PokerCard.KING in ranks:
                    ranks.remove(PokerCard.KING)
        elif self.penultima_round:
            if len(ranks) > 1:
                if PokerCard.ACE in ranks:
                    ranks.remove(PokerCard.ACE)

        self._ran.shuffle(ranks)

        return ranks

    @property
    def smaller_ranks(self):
        ranks = self._select_rank(lambda x:x.val < self._session_status.current_rank
                                and x.val not in self._session_status.exclude_ranks)
        if self.first_round:
            if len(ranks) > 3:
                if PokerCard.TWO in ranks:
                    ranks.remove(PokerCard.TWO)
                if PokerCard.THREE in ranks:
                    ranks.remove(PokerCard.THREE)
                if PokerCard.FOUR in ranks:
                    ranks.remove(PokerCard.FOUR)
        elif self.second_round:
            if len(ranks) > 2:
                if PokerCard.TWO in ranks:
                    ranks.remove(PokerCard.TWO)
                if PokerCard.THREE in ranks:
                    ranks.remove(PokerCard.THREE)
        elif self.penultima_round:
            if len(ranks) > 1:
                if PokerCard.TWO in ranks:
                    ranks.remove(PokerCard.TWO)

        self._ran.shuffle(ranks)
        return ranks

    @property
    def poker_suits(self):
        suits = list(PokerCard.non_joker_suits())
        self._ran.shuffle(suits)
        return suits

    def valid_round(self, round):
        return round == self.current_round

    def delete(self):
        self._session_status.delete()

    def begin(self):
        poker_ranks = self._select_rank(lambda x:x not in 
                                        (PokerCard.TWO, PokerCard.ACE,
                                        PokerCard.THREE, PokerCard.KING,
                                        PokerCard.FOUR, PokerCard.QUEENE,
                                        PokerCard.FIVE, PokerCard.JACKY))

        self._ran.shuffle(poker_ranks)
        poker_rank = self._ran.choice(poker_ranks)
        poker_suit = self._ran.choice(self.poker_suits)

        self._session_status.exclude_ranks.append(poker_rank.val)
        self._session_status.current_rank = poker_rank.val
        self._session_status.save()
        
        self.statistics.incr_total_rounds()

        resp = {}
        resp['suit'] = poker_suit.name
        resp['rank'] = poker_rank.name
        resp['round'] = self.current_round
        return resp

    def gaming(self, choice):
        bigger_ranks = self.bigger_ranks
        smaller_ranks = self.smaller_ranks

        if self._player_win(choice):
            if self.last_round:
                self.status = settings.TURNER.status.win
                self.statistics.incr_win_rounds(self.current_round + 1)
            else:
                self.status = settings.TURNER.status.updating

            if choice == settings.TURNER.large:
                poker_rank = self._ran.choice(bigger_ranks)
            else:
                poker_rank = self._ran.choice(smaller_ranks)
        else:
            self.status = settings.TURNER.status.lose
            if choice == settings.TURNER.large:
                poker_rank = self._ran.choice(smaller_ranks)
            else:
                poker_rank = self._ran.choice(bigger_ranks)

        self._session_status.current_round += 1
        self._session_status.exclude_ranks.append(poker_rank.val)
        self._session_status.current_rank = poker_rank.val
        self._session_status.update_expire_time()
        self._session_status.save()

        poker_suit = self._ran.choice(self.poker_suits)

        resp = {}
        resp['status'] = self.status
        resp['suit'] = poker_suit.name
        resp['rank'] = poker_rank.name
        resp['round'] = self.current_round
        resp['award_currency'] = self.award_currency
        return resp

    def end(self):
        if self.award_currency > 0:
            self.status = settings.TURNER.status.win
        else:
            self.status = settings.TURNER.status.lose
        self.statistics.incr_win_rounds(self.current_round)

        self._session_status.save()
