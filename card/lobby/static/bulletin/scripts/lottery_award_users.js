var LotteryAward = function(){
    var get_lottery_version = function() {
        return "幸运大抽奖获奖玩家公告（" + lottery_version + "期）";
    };

    var get_lottery_users = function(){
        var result = '<table border="1">';
        var data = lottery_users;
        result += "<tr><td>昵称</td><td>奖励金币</td></tr>";
        for (var idx in data) {
            var row = data[idx];
            var tr = '<tr>';
            var tr = '<tr>';
            tr += '<td>' + row.name + '</td>';
            tr += '<td>' + row.award + '</td>';
            tr += '</tr>';
            result += tr;
        };
        result += '</table>';
        return result;
    };

    return {
        get_lottery_version: get_lottery_version,
        get_lottery_users: get_lottery_users,
    };
}();