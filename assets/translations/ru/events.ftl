event-error =
    .general =
    #ErrorEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Произошла ошибка!</b>

    { frg-build-info }
    
    { $telegram_id -> 
    [0] { space }
    *[HAS]
    { hdr-user }
    { frg-user-info }
    }

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

    .remnawave-version =
    #RemnawaveVersionWarningEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Событие: Возможная несовместимость с Remnawave!</b>

    <blockquote>
    Версия панели <b>{ $panel_version }</b> выше протестированной версии <b>{ $max_version }</b>. Некоторые функции бота могут работать некорректно.
    </blockquote>

    { frg-build-info }
    
    .remnawave =
    #RemnawaveErrorEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Ошибка при подключении к Remnawave!</b>

    <blockquote>
    Без активного подключения корректная работа бота невозможна!
    </blockquote>

    { frg-build-info }

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

    .webhook =
    #ErrorEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Зафиксирована ошибка вебхука!</b>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

    .channel-check =
    #ChannelCheckErrorEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Событие: Ошибка проверки подписки на канал/группу!</b>

    { hdr-user }
    { frg-user-info }

    <blockquote>
    • <b>Причина</b>: <code>{ $reason }</code>
    </blockquote>
    
    Проверьте, что бот является администратором канала/группы с правом просмотра участников.

    .notification =
    #NotificationErrorEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Событие: Ошибка доставки системного уведомления!</b>

    <blockquote>
    • <b>Маршрут</b>: { NUMBER($chat_id, useGrouping: 0) }{ $thread_id ->
        [0] { space }
        *[HAS] :{ NUMBER($thread_id, useGrouping: 0) }
    }
    • <b>Причина</b>: <code>{ $reason }</code>
    </blockquote>

    Проверьте маршрут уведомлений и убедитесь, что бот является участником группы с правами на отправку сообщений.


event-bot =
    .startup =
    #BotStartupEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Бот запущен!</b>

    { frg-build-info }

    <b><tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Доступность</b>:
    <blockquote>
    • <b>Режим</b>: { access-mode }
    • <b>Платежи</b>: { $payments_allowed ->
    [0] запрещены
    *[1] разрешены
    }
    • <b>Регистрация</b>: { $registration_allowed ->
    [0] запрещена
    *[1] разрешена
    }
    </blockquote>

    .inline-mode-disabled =
    #BotInlineModeDisabledEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Событие: Inline-режим отключен в BotFather!</b>

    <blockquote>
    Бот не настроен для работы в inline-режиме. Некоторые функции бота могут работать некорректно.

    Включите Inline Mode в BotFather: <b>@BotFather → /mybots → Bot Settings → Inline Mode → Enable</b>
    </blockquote>

    .shutdown =
    #BotShutdownEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Бот остановлен!</b>

    { frg-build-info }

    <blockquote>
    • <b>Аптайм</b>: { $uptime }
    </blockquote>

    .update =
    #BotUpdateEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Обнаружено обновление Remnashop!</b>

    <b><tg-emoji emoji-id="6050643982646513651">📑</tg-emoji> Версии</b>:
    <blockquote>
    • <b>Текущая</b>: { $local_version }
    • <b>Последняя</b>: { $remote_version }
    </blockquote>


event-user =
    .registered =
    #UserRegisteredEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Новый пользователь!</b>

    { hdr-user }
    { frg-user-info }

    { $referrer_user_id ->
    [0] { empty }
    *[HAS]
    <b><tg-emoji emoji-id="5891207662678317861">🤝</tg-emoji> Пригласитель</b>:
    <blockquote>
    { $referrer_telegram_id ->
        [0] • <b>Почта</b>: <code>{ $referrer_email }</code>
        *[HAS] • <b>ID</b>: <code>{ NUMBER($referrer_telegram_id, useGrouping: 0) }</code>
    }
    • <b>Имя</b>: { $referrer_name } { $referrer_username ->
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_telegram_id }">@{ $referrer_username }</a>)
    }
    </blockquote>
    }

    { $ad_link_id ->
    [0] { empty }
    *[HAS]
    <b><tg-emoji emoji-id="6032949275732742941">🎯</tg-emoji> Рекламная ссылка</b>:
    <blockquote>
    • <b>Название</b>: { $ad_link_name }
    • <b>Код</b>: <code>{ $ad_link_code }</code>
    </blockquote>
    }

    .first-connected =
    #UserFirstConnectionEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Первое подключение пользователя!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-subscription }
    { frg-subscription-details }

    .device-added =
    #UserDeviceAddedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Пользователь добавил новое устройство!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

    .device-deleted =
    #UserDeviceDeletedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Пользователь удалил устройство!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }


event-blacklist =
    .registration-attempt =
    #BlacklistRegistrationAttemptEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Попытка регистрации из черного списка!</b>

    { hdr-user }
    { frg-user-info }


event-subscription =
    .trial =
    #SubscriptionTrialEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Получение пробной подписки!</b>

    { hdr-user }
    { frg-user-info }
    
    { hdr-plan }
    { frg-plan-snapshot }
    
    .new =
    #SubscriptionNewEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Покупка подписки!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

    .renew =
    #SubscriptionRenewEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Продление подписки!</b>
    
    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

    .change =
    #SubscriptionChangeEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Изменение подписки!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot-comparison }

    .expiring =
    { $is_trial ->
    [0]
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Внимание! Ваша подписка закончится через { $duration }.</b>
    
    Продлите ее заранее, чтобы не терять доступ к сервису! 
    *[1]
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Внимание! Ваш бесплатный пробник закончится через { $duration }.</b>

    Оформите подписку, чтобы не терять доступ к сервису! 
    }

    .expired =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Внимание! Доступ приостановлен — VPN не работает.</b>

    { $is_trial ->
    [0] Ваша подписка истекла, продлите ее, чтобы продолжить пользоваться VPN!
    *[1] Ваш бесплатный пробный период закончился. Оформите подписку, чтобы продолжить пользоваться сервисом!
    }

    .expired-ago =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Внимание! Доступ приостановлен — VPN не работает.</b>

    { $is_trial ->
    [0] Ваша подписка истекла { $duration } назад, продлите ее, чтобы продолжить пользоваться сервисом!
    *[1] Ваш бесплатный пробный период закончился { $duration } назад. Оформите подписку, чтобы продолжить пользоваться сервисом!
    }

    .limited =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Внимание! Доступ приостановлен — VPN не работает.</b>

    Ваш трафик израсходован. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Продлите подписку, чтобы сбросить трафик и продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете продлить подписку, чтобы сбросить трафик.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Оформите подписку, чтобы продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете оформить подписку, чтобы пользоваться сервисом без ограничений.
        }
    }

    .not-connected =
    <b>🔌 Не получилось подключиться?</b>

    Если у вас возникли сложности с настройкой VPN — мы готовы помочь! Напишите в поддержку, и мы разберемся вместе.

    .revoked =
    #SubscriptionRevokedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Пользователь перевыпустил подписку!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-subscription }
    { frg-subscription-details }


event-node =
    .connection-lost =
    #NodeConnectionLostEvent
    
    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Соединение с узлом потеряно!</b>

    { hdr-node }
    { frg-node-info }

    .connection-restored =
    #NodeConnectionRestoredEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Соединение с узлом восстановлено!</b>

    { hdr-node }
    { frg-node-info }

    .traffic-reached =
    #NodeTrafficReachedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Узел достиг порога лимита трафика!</b>

    { hdr-node }
    { frg-node-info }

    .billing-payment =
    #NodeBillingPaymentEvent

    <b><tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Событие: { $reminder ->
        [in-7-days] Оплата узла через 7 дней
        [in-48hrs] Оплата узла через 48 часов
        [in-24hrs] Оплата узла через 24 часа
        [due-today] Оплата узла сегодня!
        [overdue-24hrs] Оплата узла просрочена на 24 часа!
        [overdue-48hrs] Оплата узла просрочена на 48 часов!
        [overdue-7-days] Оплата узла просрочена на 7 дней!
        *[OTHER] Напоминание об оплате узла
    }</b>

    { hdr-node }
    <blockquote>
    • <b>Название</b>: { $node_name }
    • <b>Провайдер</b>: { $provider_name }
    • <b>Дата оплаты</b>: { $next_billing_at }
    </blockquote>


event-torrent-blocker =
    .user-blocked =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Доступ на сервере временно ограничен.</b>

    На ноде <b>{ $node_name }</b> зафиксирован BitTorrent трафик.
    Ограничение будет действовать еще <b>{ $block_duration }</b>.

    Если нужна помощь с настройкой подключения, обратитесь в поддержку.

    .report =
    #TorrentBlockedEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Событие: Обнаружен BitTorrent трафик!</b>

    { hdr-user }
    { frg-user-info }

    <blockquote>
    • <b>Нода</b>: { $node_name }
    • <b>IP</b>: <code>{ $blocked_ip }</code>
    • <b>Длительность блока</b>: { $block_duration }
    • <b>Разблокировка</b>: { $will_unblock_at }
    • <b>Протокол</b>: <code>{ $protocol }</code>
    • <b>Источник</b>: <code>{ $source }</code>
    • <b>Назначение</b>: <code>{ $destination }</code>
    </blockquote>


event-referral =
    .attached =
    <b><tg-emoji emoji-id="6041731551845159060">🎉</tg-emoji> Вы пригласили друга!</b>
    
    <blockquote>
    Пользователь <b>{ $name }</b> присоединился по вашей пригласительной ссылке! Чтобы получить награду, убедитесь, что он совершит покупку подписки.
    </blockquote>

    .reward =
    <b><tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> Вам начислена награда!</b>
    
    <blockquote>
    Пользователь <b>{ $name }</b> совершил платеж. Вы получили { $reward_type ->
    [POINTS] <b>{ $value } { $value -> 
        [one] балл
        [few] балла
        *[more] баллов 
        }</b>

    <i>Для использования баллов перейдите в раздел "Пригласить" в боте, чтобы узнать о доступных наградах и способах их использования.</i>
    [EXTRA_DAYS] <b>{ $value } доп. { $value -> 
        [one] день
        [few] дня
        *[more] дней
        }</b> к вашей подписке!
    *[OTHER] <b>{ $value } { $reward_type }</b>
    }
    </blockquote>

    .reward-failed =
    <b><tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Не получилось выдать награду!</b>
    
    <blockquote>
    Пользователь <b>{ $name }</b> совершил платеж, но мы не смогли начислить вам вознаграждение из-за того что <b>у вас нет купленной подписки</b>, к которой можно было бы добавить { $value } { $reward_type ->
    [POINTS] { $value -> 
        [one] балл
        [few] балла
        *[more] баллов 
        }
    [EXTRA_DAYS] доп. { $value -> 
        [one] день
        [few] дня
        *[more] дней
        }
    *[OTHER] { $reward_type }
    }.
    
    <i>Купите подписку, чтобы получать бонусы за приглашенных друзей!</i>
    </blockquote>

event-promocode =
    .activated =
    #PromocodeActivatedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Событие: Активация промокода!</b>

    { hdr-user }
    { frg-user-info }

    <b><tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Промокод</b>:
    <blockquote>
    • <b>Код</b>: <code>{ $promocode_code }</code>
    • <b>Тип</b>: { promocode-type }
    • <b>Награда</b>: { frg-promocode-reward }
    </blockquote>

event-payment =
    .refunded =
    #PaymentRefundedEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Событие: Платеж возвращен!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    Требуется ручная проверка — подписка пользователя могла остаться активной.

    .referral-failed =
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Не удалось начислить реферальную награду</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    Покупка завершена успешно, но при начислении реферальной награды произошла ошибка. Требуется ручная проверка.

    .purchase-failed =
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Событие: Ошибка обработки платежа!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    Платеж получен, но не удалось выдать подписку. Транзакция помечена как FAILED. Требуется ручная проверка.

event-remnashop-welcome =
    <b><tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Remnashop v{ $version }</b>

    Проект создан и поддерживается всего одним <strike>разработчиком</strike> электриком. Поскольку бот полностью БЕСПЛАТНЫЙ и имеет открытый исходный код, он существует только благодаря вашей поддержке.

    <tg-emoji emoji-id="6034923938486684992">⭐</tg-emoji> <i>Поставьте звездочку на <a href="{ $repository }">GitHub</a> и присоединяйтесь к нашему <a href="https://t.me/@remna_shop">сообществу</a>.</i>

    <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> <i>Также есть <a href="https://boosty.to/snoups/purchase/3778398?ssource=DIRECT&amp;share=subscription_link">приватный чат</a> для донатеров.</i>