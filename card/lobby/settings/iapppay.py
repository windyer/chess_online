# -*- coding:utf-8 -*-

from go.util import DotDict
from card.core.property.three import Property

IAPPPAY = DotDict({
    'appid_iapp_pay': '300322047',
    'appid_holytree_pay': '300338386',
    'appid_zx_pay': '300383663',
    'appid_zx003_pay':'3004415512',
    'appid_zx010_pay':'3004752644',
    'appid_sj04_pay':'3004907911',
    'appid_lenovo_duowan':'3005020811',
    'appid_fg_pay':'3005730751',
    'appid_sj_pay': '3006168346',
    'appid_hy_pay': '3006513135',
    'appid_ly_qmzjh_pay': '3008259240',

    'create_iapppay_order_url': "http://ipay.iapppay.com:9999/payapi/order",
    'login_url':'http://ipay.iapppay.com:9999/openid/openidcheck',
    'app_conf':DotDict({
        '300322047':DotDict({
            "appvkey": "MIICXAIBAAKBgQCrTjUffjxC55DvaVMhgAeL+RMFfqN6QHVNnW2AXmYYxSp+l13cSweyURtMFbl4JfTzGo6OW9UI05Hi0hJzMs8NvoifuEtxPvzUAC/ar80sKnKQNA4scCRdDf7Ttdu7heVh8sc5dKkh8ene1U+lcziIeLjZc5fpyhqbuh8OHQM3IwIDAQABAoGAU+HA24H5yh0P+FuPrFi/2UeGi+s965ACoJXU18XhooFxVHmUKVnIFAXpIvGEVxPnBN9dLNJE18SZrAKHrEcV4WszyphC5iS0VxohViqkLV5p0HKjmSaTM0inSh8eHs2XoNn9Cj9AaLE8cZ2PsfERl9u/bBN38e6AVNwhf4iAaMkCQQDunIODsxBn/xO/gDQ9hCRVc8aC9/Cp+JRStrBGGm/bLSvS+aHvGyIUlGC6660krj8I4O/oNFWXRLf+tTs8LqflAkEAt8oMdTMWS4MRxOQCysA+Vhc3KzYQjTfa23EWeFxTzEz1+1DTJlkiXoqbUu5lckIh9FYdY9JCzW8LDG+kUphiZwJAdripNv4BS70+timz1GfLLDlOrBtxQyDLq9v6GOdOgF8ZTv+l8rItYs/w0RAyNe38rw48T+y6KWmnorPJpUgRgQJBAKO881pa2EsQC32hMceWfDLQ3gq2UQqvL2F/n+g9QT7rdd6fxG4OzSrzS6wXzfN8bam0Ktzqzy8c9ffvYrNfJZMCQHL4ZR0azzxuTtapSnqY62CzooPzIj063aCZn8hLOxtj0CgTUkSCGrP+4mOLNkaNxVk9IqTukr3+kmFc0H4xKho=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+d2EivFCMepQfpJZhkaTCu5ipURBjZB3PQy/ijPHiUJcfRi8iEyktxptNWjmZJwPKvz7h/i7sm8jcmnvTwheWhjvTxQlTCqgbYbDLc642f5JhVnFqgF5wg4TE07D6iXO4e/4Pk9dnvOn9E/LWjERf9rDlaKf0ykPvlq+7AbB83QIDAQAB", 
            'notify_url':'http://120.27.103.99/three/iapppay/order/notify/',
            }),
        '300338386':DotDict({
            "appvkey": "MIICXAIBAAKBgQCbHcvd3qIaylCtuE1VL6JTAfeHM/vXj7GHXCxauk24vl4jOQ6mZurhHPlEGIj7Zc/QWPsahsYIEXpLTji/VOM/9u2Emih/6OXxg5yLEU3QRWRuhy5+nSW10C+5Zyc8NWGHOaHuq6owFDFgqY5AL7/exkB/NV78pEfNA3zfUPXpqwIDAQABAoGAYkuddvmwC/4M5ikWiFbpLGTgsMLWYqFiRH66dLv+qIWqLfPoPraVPRYZN3e8xmKcMFFSvlqNf2tj7fihqU1nu5JhLiP32d/qE+38XtctQpWrm/PggqHpzT5di6XHDVvnyIug9yuXzz9k4QC2aQ1VkBw8m3Pmgzssr9lBzzIB52ECQQDMYREi1yDxkOauz8N9E2xy5WXnQVuype7kjmQu/viFN+3lvdeuGCiJpXQz+ho4CW0BTxKep6ZPGAi4FNAWfPqDAkEAwktzyrhD23uIW+fJPwNoFQgXXECu3aZ036eItQPwFUX2wZepMKQfVwmfOWHvoB2GoViwZ4LDBa5WJxOhrdXLuQJAMPxi+xLNFplAcU3i8SuiprdNAWys6djTtXxbjtgWAPgy0Qn7lAK+VJ+PhpW/iwbXVaT6NYTBW9vK2zRB2+IAuQJBAKpqF5O07v+xaDaEJIV6bW4U/LhTm4yZlWUdwtBSNd/Sz82ZQjKBoWNr8xYXil+7xfv6mC8SCBARi0sW8vZP0TECQHQLKutx8kXSvbmXDJG5+0mmkiRHaLd4FHwIUgs9V+Gkzr7F/l3HprG3PVqoUw5gmJVQblf+ulXJiGsKtTPfPyQ=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCjUCc+qbMtJ5Z9E3n03oj9OR4wgHlA8Ko5uiOf7K8ch5np0fDwcreojwUgPSzOm9ISxeM1Er17tyeVte1qybN6+NyIRIHXTxcuWC6vw1RPmeVskwlBWv9Dkv5I7o4+GqJ3ARYrGeZ6GLHs/5zfX+z8f+VdcLSX8l1DYc1XEixGSQIDAQAB", 
            "notify_url":"http://120.27.103.99/three/iapppay/order/notify_holytree/",
            }),
        '300383663':DotDict({
            "appvkey": "MIICXAIBAAKBgQCcon2+Nn0n++cAQnKyWJp/JAIwCVGxTziXVcfpgyRNVoeYnf5B7hIx+58tmhL9ov7xq9jEh91u4JhjlNxqUqK32OWUATPhKJTUAof+SK23AyLBGspGBV2HULoyRJf50UN5938bWyYltsDct6hQrgIG3jcg9pzxP8UBuC6wHR6e5wIDAQABAoGAMg+1BKBBrA/Uqr6SDfJHnq8Ri+zOkU7ylVuzQyzI43bua5bDdqryYcs7+sUtoKcBuJfl9ho+aXua+OjQ8aJrorp50DdCuQTx7MRUwQm2nuq/sSw8GmlIglBpcAkF1pSziuYyYXBBzFFeKo21DStIrXrf+x8yhY2xRPa4D+NOt7ECQQDXEpPB4s7EPjrESVSX29Dao3a4H4rQthlq2QdL9k6yRbJaOntahK0vXhb5aQurQqMG8sFSgN5YGBEOjSjI1KuNAkEAunESFAPmOd4q4FAl3ApuDIzuYTvMINfhwBesDaec9iTrTjN+jjf23VlKCNq+9PBRMhtbX5kYQWxTu8e6FRHdQwJBAMr2jhgfyU7rBxxrs3goCh36uzOhGKhD4RKzQy6Nf9C+80QxAm323VThLz8pwchZ9228M3J/iNSLybT4w69a+5UCQGSqEkG+TTsnam0MuTRSaVLbcQYM3E1LYnduEJaazlPUYTwq74ToUKD4ydF4Eix76MsuHCrEpWUFkTxNPXqM17MCQGlGi85thY6gY7X+eeuZhVZFXxococltjEhaH/nI5t30Ivp8Wu7BDMNqwQ2CmqPHh9Qy315A7yJ80TrJ2gGiSe4=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCNMHZ7wB9HGsAOIH1oCmYsCAFVC/2v4C1JfB48u7EuRTXJF03RQAnGs160RWBa/gwPj2xTCMdaK6AEZPT4xzJajJl+axSbc/KgtTPEZtWwcvB0eOZvSOVmlwgaQq0akNB5GpKhLOLrPivFnuxYqppRCS44wY0tVH0qScVQodJImQIDAQAB", 
            "notify_url":"http://120.27.103.99/three/iapppay/order/notify_zx/",
            }),
        '3004415512':DotDict({
            "appvkey": "MIICXAIBAAKBgQCRo/Qie2163z0aSNoqjbfIRAKgYIJ1Phfx94hZlJArJr5GGnjCeCIRSb72r/PxRV20ZUcCY4CMdcUPEUEEeH34cj+j98Dlla2Kxyj2Q4gQafOoYK/YdwHstTiN/gTLuI3r7kOSVjemswjoNckqTvmofvCQ4N1vPujj43MnG5jfWwIDAQABAoGAawWfHkOzFMq9HPaSExknBywq/e1NkJg7glySvrk0I/GJevxy5vzek/OsN5ze1tpRXIHb53509UKJt2PHcmCUuAHU5VcJQSVKZ2JfvU4xi6v/zUb1jV7V5YvQc1QnJHOiQPThies+bpm0wpTSpaGsIXOVoBPnji5+1RZ6uNrnFPECQQDdWnWDpOIgHe/AB8UuUYc4YpRlpbKWXzJzzE8xUDsmgBH1u7fn2k1xVTWLR+259av/MsWRnIcjF6hjr558uBbDAkEAqG+1VcpqifL8GtQ+NS6+aAzlUK1HzkH9bpG93muOK0P3u5weK6k7QQOpLKNMIltNQG5BvF22TixQc7bM/Pd7iQJAM35txBhBepM8SQIFvwa8XEOinhrz9sNiq0mmSqSNfiFhDDeFSuygA3N9J0+uYApk3tNi3sL5NRK126rpRb5VnQJAKz6S9fXEKKrD4zd+yTS5GgnFjlMOznvOz2aHsuU2WRFYN0i7zkXiuqxv8M/0KhX63YHxSqVcuvFRroPOWVxI0QJBAJXVfap642Rr735CrQbh1lmapUYfEFKxF7Ad0fE/ZMCG7JcXlZzdtv/RR0+7pJ5OPx7TUaDRoOXJKC8zYLV/N6Y=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCOTIP38Ynpz6gBynFGS04Fc4gxW6iRRBqBpPqgpzevfR1NrPNA7h5+WJMhfWu9S+j4lFC88EXXRSJvzPFzEg5qaWuXBQigTXiWFCwGlb/pTNpOsEoANrejZMjTfoKxZV6eoHkcb2FXSbCBxvwN2rBYeCRdwOzP2d7Mz4Nv7C1TewIDAQAB", 
            "notify_url":"http://120.27.103.99/three/iapppay/order/notify_zx003/",
            }),
        '3004752644':DotDict({
            'appvkey':'MIICXgIBAAKBgQCe09wQ02Ym4a6UTgof+EpGUOSFGS1MuUS5iWrxk+lrfQDXUCZX8pYITxrAsLCoLPyDIfkpl6JpXTftRpF98AnmE0nXQzqFkZ/jTKX10sJ5NtYyi7myjIzg4+2ePIjuBJr44HytewL18aITw9QrUET03d0u5EhRWRou9vh92GUR3wIDAQABAoGBAJm+POTwrY5voX2fuT9PKh68yShpwabmJDdxZNsqMaZB36GMzUEO6tpqMFxb7PUubtRE+5qeVLGnca62Q7njtL+9Nkjq+y7OBo7ojLu4AmQOB7doo9ArsWhK+WbUdwk21X/mhtrTIYEOxhw2CIuBhibAg3XdFv54vathQAKaOWRBAkEA7b09Wv6eubaiJVHzEfAONXH60KpabI9h1eddukaCMpe29mjsZNL4mpvTHoaVdZv9qURNWWcvPW40Ah6MO38d/wJBAKsG8vqXKqUXnPZCbXQa45Smtfa656MMeLzmBbKl7TszLLAtuoBBgqvrf4EO7xy9mfcqdaibzJqJB4oATPTlzCECQQDQDSFJpbQwYCTsNhhbJVK58OKHg92YTa5X7J84qgW80sqaP95IqdxIKYALocngX8AQRqbOS5+qyeuXwzYDx03vAkAIkUGMwhPVz1gCkhNPlKU/5hYJdRVzeoV12QQCDgPTSl37uV61XBLCr/pkKa5avzi+Q/c+6gcW2rRw+lDgl75hAkEAxz6G5QqDAqK72MMmrovgIfE3t0MRrdMfdUQ2Oir4F0WM7mDz9Exd6IkzB9kaVHolH2TpKsoHxljgUmyarikG0Q==',
            'platpkey':'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCVlds8iZm9fIaNm8NpwW2AhPXWxOQGTfBQsnBEFmMGmZtcAfmfkQL9FgNEKeTIoobmHQbtKsjL3q7JngL2vWUVCN43th5Qy3gScpTZhw8Q7xRiPzd7UReM6eJ/N4ruYJcVg+qhmfJLeu5ctYa7NluSMoHWdSx+A7ovRmLpdS/KtQIDAQAB',
            'notify_url':'http://120.27.103.99/three/iapppay/order/notify_zx010/',
            }),
        '3004907911':DotDict({
            'appvkey':'MIICXAIBAAKBgQCgidj6aOBunviEhD0T+RqqkBVn1EUM41YZB367vGto9uP6P0YRJwduwzRKJUDGiz63ho1KgImna2utA9ZU2BneEkLGEqXJ0WtCCpubI1qcP9fjAlCe43usK++IwJ6puMKc1G6nD2L/4qioNGdwG8Il1sXe0zZSXliUoPbjZ/4ePwIDAQABAoGAcnEyM3iWHWXIJbebTuSypMpn6AeDXeemFduo9a4hJ8dwx5FZopqfCs+vM/gQkDjtcalCiczN1IKYVNM6dGtFLE+oEYAW9SzL9T6v+W+gaBtOdZl10elRsNzSnXPbJNgRF/33PVxqwA+mHZsUJnKuR5SYQcxSfjkTqYHbD9CJFukCQQDT6n5+ZulWVGKHowYUJbE2crreWK7nLgw/wiKxNw0UvYQOJHaLgq2NbCqTn8CNMbfjS6NwNiiodfakCPTuOd0LAkEAwe9DRtmDrLj5lz/s8spf9LIZ9x2tvgZNN3P6wE3LNd1NxzK5ZYvVwhvf/DlzH6dZXtm7taciJUN57fpgoNS8HQJAXPefvLZLIXttqlGDpi0O/HMCte6z9GmIKCRz8cjT7Uhi+Y1XkEao+sT8PL01zPuFz6psLhskZRszM61WPniWFwJBAIInIECZVDyD+8XdOhmLZjCjords7KB+PC4+IQgUbY/d0Qgh67jRywi1inIM4E1bE6iLeeWkoE7f5SGoilcFzqUCQGXJW1nOes0XYCICWhTSL16oGoI7Ctb5m3r2s67ZhOr5sVrugw+yK4LY+s2IVGrNbbpzqM7z7IoHMg979Ttdc/E=',
            'platpkey':'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCoh8HffWyV4F9tQU0leiaR1c7uFudA3XIJ0xV68y1G9ilTf5VW10snBE9gkuKlA1yAeFUa/btaqtgSVID3rXZm7r8mYPV0rwjtORiFZuPB6ejwnxduw+ZM6IBj0MJiM7ydHpYfliD3iCDQchb+fIAIvwVi1Z4hsBo+co6YoUJm1wIDAQAB',
            'notify_url':'http://120.27.103.99/three/iapppay/order/notify_sj04/',
            }),
        '3005020811':DotDict({
            'appvkey':'MIICXAIBAAKBgQCEQx24tiNnsnY5zDW6SQBrSPIVvjuGSwt1PpfqPta17S81osWaLW0i+TTtF2/N2+NwoRotqbwATrQ8IRkmZeAzsLUuNhhuUPkSJYjAmaRhBVXuhyCfk/acWxxUPb9WZeGIlo5Of6MqihxVQLdXjrSX/lg0Nz9LnNDL3ilGDdaNPwIDAQABAoGAMKD8rI1LNzVGgrmyh2uP2+JWH+hxuk6dR95bvKSeDQXH9dCDFszc857s9r9HPEk8toyFM4TUusg1PGZu+M88PzuMJw6Odkocdd6G+g4bktwkVETroM793I+OS+NK4mrKF80AoT3CuMcqfenLnAlS+OSwN6tCPUsgs4LVXq6k/gECQQDcroMW0Q6gFgtATjacuEVW+HN05k5kQORKA7tjLoIv7JkDbFH46sOBU0xUl5JdTV+UlSqSECh8elEtuiEgsJOpAkEAmW3+IcUcy4unaoghu2robuI8avZC9vLKn236lEoNxqcN7U5fIrnc5mnJz84dXRmuz/9AbdVLGeZNb2emEtiqpwJAXkiw+S6YcQz6AZ9o9cxE08OSkH9VPr/6ySSPCvDz7kXHmg7NduvWW4qbMgkQH4zPKUwRxBXjNkuMI11CihTnAQJASXgIFveiQD2RX0vsiyg4QNCIidd+XW4JZKpvMQ785cEcxCOhHqnNg2/ouV9DZE9mDCd4HJ/kJHTJY61IMwIZRQJBANIN50GMJ0+kZt0ovDPmaGRBn8GhdXyPLCXEcSJ4hvPSHnY8wAJoeS6SAyaEpgx5kgvx6bWE6DbrKny6brQ0708=',
            'platpkey':'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCqktdNDjN9WTx5J97tYx5gPtIVNe+/IzZ8v/0lyWgONa/8dC5AOxcZR737DBmg7RPZJFYdzGpY4ROj6QWO4/Yt+jnRyrvIGDTzvS0Gq+T0BK0GGkloRbALiM0wborHlhH/wKes4UWYYU7i45ujiwlgKIWIO64mqKiXbi2wQohXIwIDAQAB',
            'notify_url':'http://120.27.103.99/three/iapppay/order/notify_lenovo_duowan/',
            }),
        '3005730751': DotDict({
            "appvkey": "MIICWwIBAAKBgQC8PfCrTVvUhPDpt8jUivyGSYHSugd9OXjPVqJkej8Lr97V1uiOYMZl9AOQH8IMu3P0FjJA4Z6UBXzDbIrB4ie+kjnKZfayq+NivtNNNPuCJWKTfRnJi0Uexc7MX0H9NoH6fvhak7CKEoFzomgEWVOlqdXl15XAffi4qRHoN/G0WwIDAQABAoGAQSqwRp1hTRE41bBqNipngZWw++Kq9Q8QY7b6QQ6RBNq9qgncOG4IQQNYuGxGIWJDohyNCSkSXOwJZR4Oa1B/sUGu3QH1BdVNdWGhD5tOEcA5Ff9elh+f2AJqnqQxxzgyd9uzhI4SFRNVDLoLyQtC0HuPHi973D9d8WbliDf/SQECQQDc+jhQiRejWP8TrV4j8VkkvaPiPPyEr5KS46G9zD382MPQt9ZxTDFe3gZSNzr8Kbse32XJRmROiTwFAzHAAEE9AkEA2hOI3fsO0imAYlHKRzoJESGdugsi+ySgZLeFdCQEE9HVZHcI/asUwlP9klnp9h/arIwN+RLtwEp35G457TT1dwJAaw7TD7mLeTkZw2e/7zvzi0hRSL9xO7twELg12SVFduVx4QHf494dITAB8f0OF7MEFA35W00+NYppSKhmhvXYpQJASBZtB/QV0iMl7VpcI29rz93s5bMIvTw+SQzhcKL3NhYHFE7FChWjpxlcmSRf0px1DNS/SbaYIRh8yWYmf+MhwQJAUBLzAt5GJJ/lvq4gDVVvUe4izq7l7h//Y5UoiZF1dSCZzdggiG2v6YtdCKNDWSIr4FMEQPCQPI1q6lbym4rX1Q==",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCM01qGxKOslve+HrYZ8eOx8docXkDJsrDut/kVZxL9an8FoV9TchBhSntkWpfOwDvoLnlUQ2iOM3rJ45K3fZyqtXf4YPF8qCtnNxAK1Mxpsbgg3c5zqmrQjHj3wpv9QVeMVetvu2PgH1S41G7ZMJZ2aIQtqbEaaHhK0E98HKWW1wIDAQAB",
            'notify_url': 'http://120.27.103.99/three/iapppay/order/notify_fg/',
            }),
        '3006168346': DotDict({
            "appvkey": "MIICXQIBAAKBgQCGEWRCHNuH/PGNlHbyAqYrCtTHu8mKk13yO/GDRZl+l+YyRriW6COwfzNRXUPKKqlXqQI+sonvB7SMO7gWGgCgRGB0L7cRMBlCo5VLewI8lbP3+Mio/bmJcNmuZ2UyUUoetzYzPsNYvupUgCJqu9TIXuWAPcyFK1lmc11jnIx4yQIDAQABAoGBAIFxUUez7RIDWoXEDoPjouRz9LVTzmeJmW9ECQ8hp+3eY1eviJHLWIoUhkvMrKMJRa9pcs1uPFcZLW0oS7irKmYbmGpMyH3fTmIiTAcILv1Zh5W5knCHqI4xq8gc5eXyvfew/QmAtLLM+bHXEb1kou8fsjpVIZ4/3gEX6IVoL8dxAkEA/ZnD3MZPAHV1EinwZBd2jboddkfMqJ7ll7ZBdiCRJOHsaQwIlgZj7v13Zp5aUaPpzuJJIe5lcUwDhz8loPztRwJBAIdWHJV5VTnuZrCDtLoIxVEm7SoHpBZ4n7JCNvga+qGCEDper9KUIN83W/CCee9cLR7nUtlnbHHXp5yaqx5RMW8CQQDl4FIId8H4+n+KXXXIZPRT+BbotqCvYIlhghXIjDDFK/1uIzhNNbG0WxG2dWgNhPVVUQ1VspFFp8+y8uybB2nVAkAIbnn7agLASDUHnDz/Nhqs8qLl8nHroHo6jduE25FvzH2cVVfY47ekkHte4ZIdMn3xJfJIbyQXd5sOq6grjF1rAkBkIFB5Oj7M4sbLAqhMNUFtG4Nu0Za5NE5gLJwUN3WxR/SB6DRuMZhH7c+OWum5ZZFe063+5zhKL4Bhhf42aB9f",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC/HM68xwFx91k74YnKM9aEAGfwqgyqd0xz6k65H8SvZj52qf+3/xlM4CYNn8Wme15W9gPSxX0AbxaLNz2I7NUIRgr22iNjOBJ6tR0mmhfYx43C21wLg1pXFOPfT9fGXeXgTM/rzzKa/vdmJKb1orELGN0atCvNSAtEm+7wvn14WQIDAQAB",
            'notify_url': 'http://120.27.103.99/three/iapppay/order/notify_sj/',
        }),
        '3006513135': DotDict({
            "appvkey": "MIICXAIBAAKBgQDFZ0H2Y0zK4Piv7AakAGaKR6+o8DjULTfSgcoNY3xB8aukVsftM3NQgioXQN4fnOxQC+OwWWjTpQXkiybPG4b9ZxwQwpsSQOuCfvqfIycDFtKrUMDmEA7vQTahCfB+/FIDZShGQr5teeqOn0UurtQ5c1sMBdfg0zoBGMPFDVSZ9QIDAQABAoGAbqxYoBHGMQx2gPMcOgB7fNV6F4Yu5k4/uMbJiD4ZoUMkDywURNmOsjl37beRkTnCh5JS4kEOc3JW3m5hoMX3JMj3uAttgM/bkAXtsWjyF1H2w96bHL8LLWA/sswKGruzP7NmC5OqG4wIXJsp9jqOGKxZBprOIrM+wd/C0Ng9jNUCQQDlFmngb6bz6El5ms4Tpm7GmgzcYH6wM4L+eAUnwyIohRhQtug3wcIdALR54NBS8BzUSCJIRNoBwmiTvFRhgUB3AkEA3Jf47C2Fh76TGt0Ldo1j8F1BFwrmAuD8ommH3kTrsYdDZJxLC4ojo4HG5EdP6X/bh5bTVbbiRaMQY39fCVof8wJBAJwuU7B3blMLIkyNhcFPzmYH0IzOHJD0DXJ/UMRy/G6zjog4qsiYiEZNnL0az+w7VuxC4Vxz1E0uxS0zUDPJcrECQAoQbOzpjsQIr9Fz8EfyX3Lh7kxM1P2goiYOxoIfhtlMoIiAkPPv03xsOVTE5CJ1EOD4wp+QfnZK4D6J2x4kHH0CQAWpZuGieKxHUODaUdBf9cdSJCJI9fQrNGJkjATppjPV8XFYi6Gh0v9qqAel/5HuHiYX/FNLaLWT1TKxT+DC86g=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCwo2KtKz6TJGP+OLuVWcyoO6Q3CwibROrM+MGddVJX9tyqc7GgCjtLbscWaMcpjt4vKewTS3bqY1Cw/oqb3RjTq45g9y/KD9IeXniYMK+WAMnOXDbY8jpamTvZG6KSCrywQNodQqxiUqwzT48eNMQaTH9ReyeKzdCxoakL4xCCuwIDAQAB",
            'notify_url': 'http://120.27.103.99/three/iapppay/order/notify_hy/',
        }),
        '3008259240': DotDict({
            "appvkey": "MIICXAIBAAKBgQCuJLta2POGLZyUcUCFL+dhWhRWf62rjVQsnShVhyCM7lSieOhE//TgFoHxysbP/rw8e1+ExpPql1oRqjP83YsnGriFVMiv8oaTfJI0HXx0PAve4MEytlZm4RIO68u49vyIFtb0NtM3NptCReCBg7DonGSFfLVO1lgA6o+416emWQIDAQABAoGAXijmVRzxsB+BhpIl/N4GEhGO5aZr1VK5rNXdNUG3S/yiLqeJj6WGVpRU9tRZ46UtSta6syRcXoAv51VMfvGbh0cQ9o30B/f1PU/nEUYpApCLQUZo5nlzU2ZmOKshr2KoH43N7mKZZWfJWTFEygihyHsL1A7iY7sQoNW1eot49/ECQQDwygCccfLcuzCPdXTE4odfQNEELD7Rt3lnewde/2wQDjKaLPi0I2MGv0bQNW/DTjXA5I605anAx4tgtybvlaYfAkEAuSTy8RL9YaQMV5EUNU0j5n1OwK4sbYXH7NH1IfokW1x5VZz6NM+AB6S5S4z+D/DV9iQMbwzb66kqvFdtOql0hwJAauMAynG6wUlHESeuogd82EfJgPSzHh04AzuV1hHEQoxK4i28aRqcRs55/Mr7xdLeAbZzstGQPUdXE6O54PipOQJBALUEVzM06d+pURfclPF4Nn2ITpM8t9ttTYdR0GYj96ALzeXS0R8JMZhHiZNAirZzNf6uSCnbXLoQb+QtZnJQc8kCQAlZXIseiFv1Culg+rF4LkvrL/Aihwi+pZO6Cwvf/9tWyXWQyJbUbuHdv3z1NKPXM4K5Z3HtbNt6+PsBOnJVI0o=",
            "platpkey": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCQ/c0/6cfo3dl35VpbjMhRA9L6LAQJu3ztLvahwY3tRtsJCVGXeOs8fdg9dWLdPtDJUw6Enq4fdgG5tbLu5K6dIoaeo0+CgFkR+FmXN5zFiSV4f7c8bYdc9kOKGjyaIDeIUvA9gf2XvP2sJFSaXzXytCMAT4H9vbci89fRhpgmZQIDAQAB",
            'notify_url': 'http://120.27.103.99/three/iapppay/order/notify_ly_qmzjh/',
        }),
        }),
    'need_validate_form':True,
    'need_auth': True,
    'iapppay_items':DotDict({
        Property.NEWBIE_COIN_BAG_ONE:DotDict({
            'pay_point_num':2,
            'order_desc':u"6元新手大礼包"
            }),
        Property.VIP_COIN_BAG:DotDict({
            'pay_point_num':3,
            'order_desc':u"30元VIP金币大礼包"
            }),
        Property.TWO_RMB_COINS:DotDict({
            'pay_point_num':4,
            'order_desc':u"2元金币包"
            }),
        Property.QUICK_FOUR_RMB_COINS:DotDict({
            'pay_point_num':5,
            'order_desc':u"快速4元购买"
            }),
        Property.SIX_RMB_COINS:DotDict({
            'pay_point_num':6,
            'order_desc':u"6元金币包"
            }),
        Property.QUICK_SIX_RMB_COINS:DotDict({
            'pay_point_num':7,
            'order_desc':u"快速6元购买"
            }),
        Property.QUICK_EIGHT_RMB_COINS:DotDict({
            'pay_point_num':8,
            'order_desc':u"快速8元购买"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':9,
            'order_desc':u"30元金币礼包"
            }),
        Property.FIFTH_RMB_COINS:DotDict({
            'pay_point_num':10,
            'order_desc':u"50元金币礼包"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':11,
            'order_desc':u"100元金币礼包"
            }),
        Property.THREE_HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':12,
            'order_desc':u"300元金币礼包"
            }),
        Property.THIRTY_RMB_COINS:DotDict({
            'pay_point_num':13,
            'order_desc':u"30元快速购买"
            }),
        Property.HUNDRED_RMB_COINS:DotDict({
            'pay_point_num':14,
            'order_desc':u"100元快速购买"
            }),
        Property.ONE_RMB_COINS:DotDict({
            'pay_point_num':15,
            'order_desc':u"1元新手金币包"
            }),
        Property.NEWBIE_TWO_RMB_COINS:DotDict({
            'pay_point_num':16,
            'order_desc':u"2元新手礼包"
            }),
        Property.NEWYEAR_SIX_RMB_BAGS:DotDict({
            'pay_point_num':17,
            'order_desc':u"6元新年礼包"
            }),
        Property.MONKEY_FIFTY_RMB_BAGS:DotDict({
            'pay_point_num':18,
            'order_desc':u"猴年大礼包"
            }),
        Property.EIGHT_HUNDRED_RMB_BAGS:DotDict({
            'pay_point_num':19,
            'order_desc':u"800元金币包"
            }),
        Property.LIMITED_GIFT_BAG:DotDict({
            'pay_point_num':20,
            'order_desc':u"6元限时礼包",
            }),
        Property.CAT_FOOD_GIFT_BAG:DotDict({
            'pay_point_num':21,
            'order_desc':u"猫粮礼包",
            }),
        Property.SUPER_BAG: DotDict({
            'pay_point_num': 22,
            'order_desc': u"30元超值礼包",
        }),
        Property.VIP_BAG_NORMAL: DotDict({
            'pay_point_num': 23,
            'order_desc': u"白银VIP礼包",
            }),
        Property.VIP_BAG_GOLD: DotDict({
            'pay_point_num': 24,
            'order_desc': u"黄金VIP道具礼包",
            }),
        Property.VIP_BAG_DIAMOND: DotDict({
            'pay_point_num': 25,
            'order_desc': u"蓝钻VIP道具礼包",
            }),
        Property.VIP_BAG_CROWN: DotDict({
            'pay_point_num': 26,
            'order_desc': u"皇冠VIP道具礼包",
            }),
        })
})
