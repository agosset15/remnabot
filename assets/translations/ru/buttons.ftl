btn-back =
    .general = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Назад
    .menu = <tg-emoji emoji-id="5960671702059848143">↩️</tg-emoji> Главное меню
    .menu-return = <tg-emoji emoji-id="5960671702059848143">↩️</tg-emoji> Вернуться в главное меню
    .dashboard = <tg-emoji emoji-id="5960671702059848143">↩️</tg-emoji> Вернуться в панель управления
    .referrals = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> К списку рефералов

btn-common =
    .notification-close = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Закрыть
    .devices-empty = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> У вас нет подключенных устройств
    .cancel = Отмена
    .next = <tg-emoji emoji-id="5773626993010546707">▶️</tg-emoji> Далее
    .prev = <tg-emoji emoji-id="5960671702059848143">◀️</tg-emoji> Назад

    .squad-choice = { $selected -> 
    [1] 🔘
    *[0] ⚪
    } { $name }

    .duration = <tg-emoji emoji-id="5891211339170326418">⌛</tg-emoji> { $value ->
    [0] { unlimited }
    *[OTHER] { unit-day }
    }

btn-devices =
    .delete-all = <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> Удалить все устройства
    .reissue = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Перевыпустить подписку
    .confirm-delete = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Да, удалить
    .confirm-reissue = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Да, сбросить
    .cancel-reissue = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Нет

    .item = { $platform_icon } { $platform } { $device_model -> 
    [0] { space }
    *[HAS] ({ $device_model }){ space }
    }— { $created_at }

btn-backup =
    .active-toggle = { $enabled ->
        [1] 🟢 Включен
        *[0] 🔴 Выключен
    }
    .set-interval = <tg-emoji emoji-id="5983150113483134607">🕐</tg-emoji> Интервал
    .set-max-files = <tg-emoji emoji-id="5805550320985578625">📁</tg-emoji> Кол-во файлов
    .send-toggle = { $send_to_chat ->
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Отправка в чат: включена
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Отправка в чат: выключена
    }
    .backup-assets = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Запустить бэкап ассетов
    .backup-db = <tg-emoji emoji-id="5778672437122045013">🗄</tg-emoji> Запустить бэкап базы данных
    
btn-remnashop-info =
    .release-latest = <tg-emoji emoji-id="6037397706505195857">👀</tg-emoji> Посмотреть
    .how-upgrade = <tg-emoji emoji-id="6030848053177486888">❓</tg-emoji> Как обновить
    .github = <tg-emoji emoji-id="6034923938486684992">⭐</tg-emoji> GitHub
    .telegram = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Telegram
    .donate = <tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> Поддержать разработчика
    .docs = <tg-emoji emoji-id="6050643982646513651">📖</tg-emoji> Документация

btn-requirement =
    .rules-accept = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Принять правила
    .channel-join = <tg-emoji emoji-id="5938368005611195877">❤️</tg-emoji> Перейти в канал
    .channel-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Подтвердить

btn-menu =
    .trial = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> ПОПРОБОВАТЬ БЕСПЛАТНО
    .trial-paid = <tg-emoji emoji-id="6028205772117118673">🚀</tg-emoji> ПОПРОБОВАТЬ ЗА { $trial_price }
    .connect = <tg-emoji emoji-id="6028205772117118673">🚀</tg-emoji> Подключиться
    .connect-reserve = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Подключиться (резерв)
    .devices = <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Устройства
    .subscription = <tg-emoji emoji-id="5886583490434044162">💳</tg-emoji> Подписка
    .invite = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Пригласить
    .support = <tg-emoji emoji-id="6032636795387121097">🆘</tg-emoji> Поддержка
    .web-cabinet = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Личный кабинет
    .dashboard = <tg-emoji emoji-id="5776424837786374634">🛠</tg-emoji> Панель управления

    .connect-not-available =
    <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> { $status ->
    [LIMITED] ПРЕВЫШЕН ЛИМИТ ТРАФИКА
    [EXPIRED] СРОК ДЕЙСТВИЯ ИСТЕК
    *[OTHER] ВАША ПОДПИСКА НЕ РАБОТАЕТ
    } <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji>

btn-invite =
    .about = <tg-emoji emoji-id="6030848053177486888">❓</tg-emoji> Подробнее о награде
    .copy = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Скопировать ссылку
    .send = <tg-emoji emoji-id="6039391666547201160">📩</tg-emoji> Пригласить
    .qr = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> QR-код
    .withdraw-points = <tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Обменять баллы
    .reset-referral = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Сбросить реф. ссылку

btn-dashboard =
    .statistics = <tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Статистика
    .users = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Пользователи
    .broadcast = <tg-emoji emoji-id="6021418126061605425">📢</tg-emoji> Рассылка
    .promocodes = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Промокоды
    .access = <tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Режим доступа
    .remnawave = <tg-emoji emoji-id="5463406057885821287">🌊</tg-emoji> RemnaWave
    .remnashop = <tg-emoji emoji-id="5920332557466997677">🛍</tg-emoji> RemnaShop
    .transactions = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Транзакции
    .importer = <tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Импорт пользователей

btn-statistics =
    .users = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Пользователи
    .subscriptions = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Подписки
    .transactions = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Транзакции
    .promocodes = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Промокоды
    .referrals = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Рефералы

    .subscription-page =
    { $page ->
        [0] { $is_current ->
            [1] [ Общая статистика ]
            *[0] Общая статистика
        }
        *[OTHER] { $is_current ->
            [1] [ { $plan_name } ]
            *[0] { $plan_name }
        }
    }

    .transaction-page =
    { $page ->
        [0] { $is_current ->
            [1] [ Общая статистика ]
            *[0] Общая статистика
        }
        *[OTHER] { $is_current ->
            [1] [ { gateway-type } ]
            *[0] { gateway-type }
        }
    }

btn-users =
    .search = <tg-emoji emoji-id="6032850693348399258">🔍</tg-emoji> Поиск пользователя
    .recent-registered = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Последние зарегистрированные
    .recent-activity = <tg-emoji emoji-id="6039614175917903752">📝</tg-emoji> Последние взаимодействующие
    .blacklist = <tg-emoji emoji-id="5938215362473496448">🚫</tg-emoji> Черный список
    .unblock-all = <tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Разблокировать всех
    .blacklist-view = <tg-emoji emoji-id="5766994197705921104">🗒️</tg-emoji> Список заблокированных
    .blacklist-block = <tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Заблокировать по ID
    .blacklist-sources = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Автообновляемые списки
    .blacklist-sources-sync = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Синхронизировать
    .blacklist-block-clear = <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> Очистить список ID

    .blacklist-source = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> { $source }

btn-user =
    .email = <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Почта
    .email-purchase = <tg-emoji emoji-id="5776182936638329359">📧</tg-emoji> Письмо: покупка
    .email-connect = <tg-emoji emoji-id="5776182936638329359">📧</tg-emoji> Письмо: подключить Telegram
    .email-custom = <tg-emoji emoji-id="6039573425268201570">📨</tg-emoji> Письмо: произвольный текст
    .email-set = { $has_email ->
        [0] <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Задать почту
        *[other] <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Изменить почту
    }
    .email-clear = <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> Удалить почту
    .password-reset = <tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> Сбросить пароль
    .discount = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Скидка
    .discount-personal = <tg-emoji emoji-id="6035084557378654059">👤</tg-emoji> Персональная скидка
    .discount-purchase = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> На следующую покупку
    .points = <tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Баллы
    .statistics = <tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Статистика
    .referrals = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Рефералы
    .message = <tg-emoji emoji-id="6039391666547201160">📩</tg-emoji> Сообщение
    .role = <tg-emoji emoji-id="6030445631921721471">👮‍♂️</tg-emoji> Роль
    .transactions = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Транзакции
    .give-access = 🔑 Доступ к планам
    .current-subscription = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Текущая подписка
    .subscription-traffic-limit = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Лимит трафика
    .subscription-device-limit = <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Лимит устройств
    .subscription-expire-time = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Время истечения
    .subscription-squads = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Сквады
    .subscription-traffic-reset = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Сбросить трафик
    .subscription-devices = <tg-emoji emoji-id="5766994197705921104">🗒️</tg-emoji> Список устройств
    .subscription-url = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Скопировать ссылку
    .subscription-delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Удалить
    .subscription-reissue = <tg-emoji emoji-id="6030657343744644592">♻️</tg-emoji> Перевыпустить
    .message-preview = <tg-emoji emoji-id="6037397706505195857">👀</tg-emoji> Предпросмотр
    .message-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Отправить
    .referral-reset = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Сбросить реф. ссылку
    .sync = <tg-emoji emoji-id="5769248574499983619">🌀</tg-emoji> Синхронизировать
    .sync-remnawave = 🌊 Использовать данные Remnawave
    .sync-remnashop = <tg-emoji emoji-id="5920332557466997677">🛍</tg-emoji> Использовать данные Remnashop
    .give-subscription = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Выдать подписку
    .subscription-internal-squads = <tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Внутренние сквады
    .subscription-external-squads = <tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> Внешний сквад

    .allowed-plan-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    } { $plan_name }

    .subscription-active-toggle = { $is_active ->
    [1] 🔴 Выключить
    *[0] 🟢 Включить
    }

    .transaction = { $status ->
    [PENDING] <tg-emoji emoji-id="5983150113483134607">🕓</tg-emoji>
    [COMPLETED] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji>
    [CANCELED] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji>
    [REFUNDED] <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji>
    [FAILED] <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji>
    *[OTHER] { $status }
    } { $created_at } · { gateway-type }
    
    .trial-toggle = { $is_trial_available ->
    [1] <tg-emoji emoji-id="6050677620830376838">🧪</tg-emoji> Пробник: доступен
    *[0] <tg-emoji emoji-id="6050677620830376838">🧪</tg-emoji> Пробник: не доступен
    }

    .block = { $is_blocked ->
    [1] <tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Разблокировать
    *[0] <tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> Заблокировать
    }

btn-broadcast =
    .list = <tg-emoji emoji-id="5766994197705921104">🗒️</tg-emoji> Список всех рассылок
    .all = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Всем
    .plan = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> По плану
    .subscribed = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> С подпиской
    .unsubscribed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Без подписки
    .expired = <tg-emoji emoji-id="5891211339170326418">⌛</tg-emoji> Просроченным
    .trial = ✳️ С пробником
    .content = <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Редактировать содержимое
    .buttons = ✳️ Редактировать кнопки
    .preview = <tg-emoji emoji-id="6037397706505195857">👀</tg-emoji> Предпросмотр
    .confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Запустить рассылку
    .refresh = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Обновить данные
    .cancel = <tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Остановить рассылку
    .delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Удалить отправленное

    .plan-title = { $is_active ->
    [1] 🟢
    *[0] 🔴 
    } { $name }
    
    .button-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    }
    
    .title = { $status ->
    [PROCESSING] <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji>
    [COMPLETED] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji>
    [CANCELED] <tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji>
    [DELETED] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji>
    [ERROR] <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji>
    *[OTHER] { $status }
    } { $created_at }
    
btn-goto =
    .subscription = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Купить подписку
    .promocode = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Активировать промокод
    .invite = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Пригласить
    .subscription-renew = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Продлить подписку
    .user-profile = <tg-emoji emoji-id="6035084557378654059">👤</tg-emoji> Перейти к пользователю
    .referrer-profile = <tg-emoji emoji-id="5891207662678317861">🤝</tg-emoji> Перейти к пригласителю
    .contact-support = <tg-emoji emoji-id="6039391666547201160">📩</tg-emoji> Перейти в поддержку
    .provider-login = 🔑 Перейти к провайдеру

btn-promocodes =
    .save = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Сохранить
    .create = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Создать промокод
    .confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Создать промокод
    .delete = <tg-emoji emoji-id="6039522349517115015">🗑️</tg-emoji> Удалить
    .regenerate = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Перегенерировать
    .code = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Код
    .type = <tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Тип награды
    .availability = <tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Доступ
    .reward = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Награда
    .plan = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> План
    .expires = <tg-emoji emoji-id="5891211339170326418">⌛</tg-emoji> Срок действия
    .max-activations = <tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Лимит активаций
    .reset = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Сбросить

    .plan-duration = { $days -> 
        [one] { $days } день
        [few] { $days } дня
        *[more] { $days } дней
    }

    .item = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> { $code } — { promocode-type }

    .active-toggle = { $is_active ->
    [1] 🟢 Включен
    *[0] 🔴 Выключен
    }

    .reusable-toggle = <tg-emoji emoji-id="6030657343744644592">🔁</tg-emoji> { $is_reusable ->
    [1] Повтор: да
    *[0] Повтор: нет
    }

btn-access =
    .mode = { access-mode }
    .conditions = <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> Условия доступа
    .rules = ✳️ Принятие правил
    .channel = ❇️ Подписка на канал

    .payments-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Платежи

    .registration-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Регистрация

    .condition-toggle = { $enabled ->
    [1] 🔘 Включено
    *[0] ⚪ Выключено
    }

btn-remnashop =
    .admins = <tg-emoji emoji-id="6030445631921721471">👮‍♂️</tg-emoji> Администраторы
    .gateways = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Платежные системы
    .referral = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Реф. система
    .advertising = <tg-emoji emoji-id="6032949275732742941">🎯</tg-emoji> Реклама
    .plans = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Планы
    .notifications = <tg-emoji emoji-id="6039486778597970865">🔔</tg-emoji> Уведомления
    .logs = <tg-emoji emoji-id="6037475557082403885">📄</tg-emoji> Логи
    .menu-editor = <tg-emoji emoji-id="5776424837786374634">🎛</tg-emoji> Редактор главного меню
    .backup = <tg-emoji emoji-id="6032745346390560408">💾</tg-emoji> Бэкап
    .extra = <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> Доп. настройки

btn-remnashop-transaction = { $status ->
    [PENDING] <tg-emoji emoji-id="5983150113483134607">🕓</tg-emoji>
    [COMPLETED] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji>
    [CANCELED] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji>
    [REFUNDED] <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji>
    [FAILED] <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji>
    *[OTHER] { $status }
    } #{ $user_id } · { gateway-type } · { $created_at }

btn-remnashop-extra =
    .device-single = { $enabled -> 
        [1] 🟢
        *[0] 🔴
    } Удаление устройства

    .device-all = { $enabled -> 
        [1] 🟢
        *[0] 🔴
    } Удаление всех устройств

    .link-reset = { $enabled -> 
        [1] 🟢
        *[0] 🔴
    } Перевыпуск подписки
    .referral-reset = { $enabled -> 
        [1] 🟢
        *[0] 🔴
    } Сброс реф. ссылки

    .trial-channel-guard = { $enabled ->
        [1] 🟢
        *[0] 🔴
    } Авто отключение пробника

    .mini-app-reserve = { $enabled ->
        [1] 🟢
        *[0] 🔴
    } Резервная кнопка подключения

    .toggle = { $enabled ->
        [1] 🟢 Включено
        *[0] 🔴 Выключено
    }

btn-menu-editor =
    .text = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Текст
    .availability = <tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Доступ
    .type = <tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Тип
    .payload = <tg-emoji emoji-id="6037475557082403885">📄</tg-emoji> Данные
    .color = <tg-emoji emoji-id="5769635757211784031">🎨</tg-emoji> Цвет
    .confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Сохранить
    .color-default = Без цвета
    .color-primary = Основной
    .color-success = Зеленый
    .color-danger = Красный

    .button = { $is_active ->
        [1] 🟢
        *[0] 🔴
    } { $text }

    .active-toggle = { $is_active ->
        [1] 🟢 Включена
        *[0] 🔴 Выключена
    }

    .subscribers-only-toggle = { $subscribers_only ->
        [1] <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> С подпиской
        *[0] <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Всем
    }

btn-gateway =
    .title = { gateway-type }
    .setting = { $field }
    .display-name = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Отображаемое название
    .webhook-copy = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Скопировать вебхук
    .test = 🐞 Тест
    .default-currency = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Валюта по умолчанию
    .placement = <tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Изменить позиционирование
    .field-reset = <tg-emoji emoji-id="6030657343744644592">♻️</tg-emoji> Сбросить значение

    .active-toggle = { $is_active ->
    [1] 🟢 Включено
    *[0] 🔴 Выключено
    }

    .default-currency-choice = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } { $symbol } { $currency }

btn-referral =
    .level = <tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Уровень
    .reward-type = <tg-emoji emoji-id="6037175527846975726">🎀</tg-emoji> Тип награды
    .accrual-strategy = <tg-emoji emoji-id="6042011682497106307">📍</tg-emoji> Условие начисления
    .reward-strategy = ⚖️ Форма начисления
    .reward = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Награда
    
    .active-toggle = { $is_enable -> 
    [1] 🟢 Включена
    *[0] 🔴 Выключена
    }

    .level-choice = { $type -> 
    [1] <tg-emoji emoji-id="5794164805065514131">1️⃣</tg-emoji>
    [2] <tg-emoji emoji-id="5794085322400733645">2️⃣</tg-emoji>
    [3] <tg-emoji emoji-id="5794280000383358988">3️⃣</tg-emoji>
    *[OTHER] { $type }
    }

    .reward-choice = { $type -> 
    [POINTS] <tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Баллы
    [EXTRA_DAYS] <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Дни
    *[OTHER] { $type }
    }

    .accrual-strategy-choice = { $type -> 
    [ON_FIRST_PAYMENT] <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Первый платеж
    [ON_EACH_PAYMENT] <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Каждый платеж
    *[OTHER] { $type }
    }

    .reward-strategy-choice = { $type -> 
    [AMOUNT] 🔸 Фиксированная
    [PERCENT] 🔹 Процентная
    *[OTHER] { $type }
    }

btn-notifications =
    .user = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Пользовательские
    .system = <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> Системные
    .route = <tg-emoji emoji-id="6048723247501938454">📡</tg-emoji> Маршрут
    .default-route = <tg-emoji emoji-id="6048723247501938454">📡</tg-emoji> Общий маршрут
    .chat-id = <tg-emoji emoji-id="6030784887093464891">💬</tg-emoji> Изменить чат
    .thread-id = <tg-emoji emoji-id="5805550320985578625">📁</tg-emoji> Изменить тред
    .route-clear = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Удалить маршрут
    
    .user-choice = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } { notification-type }

    .system-choice = { $enabled -> 
    [1] 🔘
    *[0] ⚪
    } { $has_route ->
    [1] <tg-emoji emoji-id="6048723247501938454">📡</tg-emoji>
    *[0] { space }
    } { notification-type }

    .active-toggle = { $is_active ->
    [1] 🟢 Включено
    *[0] 🔴 Выключено
    }

btn-plans =
    .save = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Сохранить
    .create = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Создать план
    .create-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Создать план
    .delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Удалить
    .name = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Название
    .description = <tg-emoji emoji-id="6030784887093464891">💬</tg-emoji> Описание
    .description-remove = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Удалить текущее описание
    .tag = <tg-emoji emoji-id="6043896193887506430">📌</tg-emoji> Тег
    .tag-remove = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Удалить текущий тег
    .type = <tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Тип
    .availability = <tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Доступ
    .durations-prices = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Длительности и <tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> Цены
    .traffic = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Трафик
    .devices = <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Устройства
    .allowed = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Разрешенные пользователи
    .squads = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Сквады
    .internal-squads = <tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Внутренние сквады
    .external-squads = <tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> Внешний сквад
    .duration-add = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Добавить длительность
    .price-choice = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> { $price } { $currency }
    .export = <tg-emoji emoji-id="5805506958995758422">📤</tg-emoji> Экспорт
    .import = <tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Импорт
    .exporting = <tg-emoji emoji-id="5805506958995758422">📤</tg-emoji> Экспортировать
    .importing = <tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Импортировать
    .url = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Скопировать ссылку на план

    .trial = { $is_trial ->
    [1] 🔘
    *[0] ⚪
    } Пробник 

    .export-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    } { $name }

    .title = { $is_active ->
    [1] 🟢
    *[0] 🔴 
    } { $name }

    .active-toggle = { $is_active -> 
    [1] 🟢 Включен
    *[0] 🔴 Выключен
    }
    
    .type-choice = { $type -> 
    [TRAFFIC] <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Трафик
    [DEVICES] <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Устройства
    [BOTH] <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Трафик + устройства
    [UNLIMITED] <tg-emoji emoji-id="6048407885233263063">♾️</tg-emoji> Безлимит
    *[OTHER] { $type }
    }

    .availability-choice = { $type -> 
    [ALL] <tg-emoji emoji-id="5776233299424843260">🌍</tg-emoji> Для всех
    [NEW] 🌱 Для новых
    [EXISTING] <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Для клиентов
    [INVITED] <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Для приглашенных
    [ALLOWED] <tg-emoji emoji-id="6037249452824072506">🔐</tg-emoji> Для разрешенных
    [LINK] <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> По ссылке
    *[OTHER] { $type }
    }

    .traffic-strategy-choice = { $selected ->
    [1] 🔘 { traffic-strategy }
    *[0] ⚪ { traffic-strategy }
    }

    
btn-remnawave =
    .users = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Пользователи
    .hosts = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Хосты
    .nodes = <tg-emoji emoji-id="5942734685976138521">🖥️</tg-emoji> Ноды
    .inbounds = 🔌 Инбаунды

btn-importer =
    .from-xui = 💩 Импорт из панели 3X-UI
    .sync-from-panel = <tg-emoji emoji-id="5769248574499983619">🌀</tg-emoji> Синхронизация: панель → бот
    .sync-from-bot = <tg-emoji emoji-id="6030400221232501136">🤖</tg-emoji> Синхронизация: бот → панель
    .sync-start = <tg-emoji emoji-id="5773626993010546707">▶️</tg-emoji> Синхронизировать
    .squads = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Внутренние сквады
    .import-all = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Импортировать всех
    .import-active = ❇️ Импортировать активных

btn-subscription =
    .plan = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Перейти к оформлению подписки
    .new = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Купить подписку
    .renew = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Продлить
    .change = <tg-emoji emoji-id="6039779802741739617">🔃</tg-emoji> Изменить
    .promocode = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Активировать промокод
    .promocode-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Подтвердить
    .pay = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Оплатить
    .get = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Получить бесплатно
    .back-plans = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Назад к выбору плана
    .back-duration = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Изменить длительность
    .back-payment-method = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Изменить способ оплаты
    .connect = <tg-emoji emoji-id="5776078972659962594">🚀</tg-emoji> Подключиться

    .payment-method = { $gateway_title } | { $final_amount ->
    [0] <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji>
    *[HAS] { $final_amount }{ $currency }
    }
    
    .duration = { $period } | { $final_amount -> 
    [0] <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji>
    *[HAS] { $final_amount }{ $currency }
    }

btn-ad-links =
    .save = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Сохранить
    .create = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Создать ссылку
    .create-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Создать ссылку
    .delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Удалить ссылку
    .name = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Название
    .code = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Код
    .regenerate = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Перегенерировать
    .stats = <tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Статистика
    .url = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Скопировать ссылку

    .title = { $is_active ->
    [1] 🟢
    *[0] 🔴
    } { $name }

    .active-toggle = { $is_active ->
    [1] 🟢 Включена
    *[0] 🔴 Выключена
    }
