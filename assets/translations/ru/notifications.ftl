ntf-error =
    .unknown = ⚠️ <i>Произошла ошибка.</i>
    .permission-denied = ⚠️ <i>У вас недостаточно прав.</i>
    .log-not-found = ⚠️ <i>Лог файл не найден.</i>
    .logs-disabled = ⚠️ <i>Логирование в файл отключено.</i>
    
    .lost-context = ⚠️ <i>Произошла ошибка. Перезапустите диалог командой /start.</i>
    .lost-context-restart = ⚠️ <i>Произошла ошибка. Диалог перезапущен.</i>

ntf-common =
    .trial-unavailable = ⚠️ <i>Пробная подписка временно недоступна.</i>
    .throttling = ⚠️ <i>Вы отправляете слишком много запросов. Пожалуйста, подождите.</i>
    .double-click-confirm = ⚠️ <i>Нажмите еще раз, чтобы подтвердить действие.</i>
    .squads-empty = ⚠️ <i>Сквады не найдены. Проверьте их наличие в панели.</i>

    .withdraw-points = ❌ <i>У вас недостаточно баллов для выполнения обмена.</i>
    .internal-squads-empty = ❌ <i>Выберите хотя бы один внутренний сквад.</i>

    .invalid-value = ❌ <i>Некорректное значение.</i>
    .value-updated = ✅ <i>Параметр успешно обновлен.</i>

    .plan-not-found = ❌ <i>План не найден или недоступен.</i>

    .connect-not-available =
    ⚠️ { $status ->
    [LIMITED]
    Вы израсходовали весь доступный объем трафика. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Продлите подписку, чтобы сбросить трафик и продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете продлить подписку, чтобы сбросить трафик.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Оформите подписку, чтобы продолжить пользоваться сервисом!
        *[RESET] Трафик будет восстановлен через { $reset_time }. Вы также можете оформить подписку, чтобы пользоваться сервисом без ограничений.
        }
    }
    [EXPIRED]  
    { $is_trial ->
    [0] Срок действия вашей подписки истек. Продлите подписку или оформите новую.
    *[1] Бесплатный пробный период завершен. Оформите подписку, чтобы продолжить пользоваться сервисом.
    }
    *[OTHER] Произошла ошибка при проверке статуса или подписка была отключена. Обратитесь в поддержку.
    }
    
ntf-command =
    .paysupport = 💸 <b>Чтобы запросить возврат, обратитесь в службу поддержки.</b>
    .rules = ⚠️ <b>Пожалуйста, ознакомьтесь с <a href="{ $url }">Условиями использования</a> перед использованием сервиса.</b>
    .help = 🆘 <b>Нажмите кнопку ниже, чтобы связаться с поддержкой.</b>

ntf-requirement =
    .channel-join-required = ❇️ Подпишитесь на наш канал и получайте <b>бесплатные дни, акции и новости</b>. После подписки нажмите «Подтвердить».
    .channel-join-required-left = ⚠️ Вы отписались от канала. Подпишитесь, чтобы продолжить пользоваться ботом.
    .rules-accept-required = ⚠️ <b>Перед использованием сервиса ознакомьтесь и примите <a href="{ $url }">Условия использования</a>.</b>
    .channel-join-error = ⚠️ Мы не видим вашу подписку на канал. Проверьте подписку и попробуйте снова.
    
ntf-user =
    .not-found = <i>❌ Пользователь не найден.</i>
    .transactions-empty = ❌ <i>Список транзакций пуст.</i>
    .subscription-empty = ❌ <i>Активная подписка не найдена.</i>
    .subscription-deleted = ✅ <i>Подписка успешно удалена.</i>
    .plans-empty = ❌ <i>Нет доступных планов.</i>
    .devices-empty = ❌ <i>Список устройств пуст.</i>
    .allowed-plans-empty = ❌ <i>Нет доступных планов для предоставления доступа.</i>
    .message-success = ✅ <i>Сообщение успешно отправлено.</i>
    .message-failed = ❌ <i>Не удалось отправить сообщение.</i>

    .sync-already = ✅ <i>Данные подписки идентичны.</i>
    .sync-missing-data = ⚠️ <i>Синхронизация невозможна. Данные подписки отсутствуют в панели и в боте.</i>
    .sync-success = ✅ <i>Синхронизация подписки выполнена.</i>

    .invalid-expire-time = ❌ <i>Невозможно { $operation ->
    [ADD] продлить
    *[SUB] сократить
    } срок подписки на указанное количество дней.</i>

    .invalid-points = ❌ <i>Невозможно { $operation ->
    [ADD] добавить
    *[SUB] списать
    } указанное количество баллов.</i>

ntf-access =
    .maintenance = 🚧 <i>Бот находится на обслуживании. Попробуйте позже.</i>
    .registration-disabled = ❌ <i>Регистрация новых пользователей отключена.</i>
    .registration-invite-only = ❌ <i>Регистрация доступна только по приглашению.</i>
    .payments-disabled = 🚧 <i>Платежи временно недоступны! Вы получите уведомление после восстановления.</i>
    .payments-restored = ❇️ <i>Платежи восстановленны! Теперь вы можете купить или продлить подписку. Спасибо за ожидание.</i>

ntf-plan =
    .not-file = ⚠️ <i>Отправьте планы в виде json файла.</i>
    .import-failed = ❌ <i>Не удалось импортировать.</i>
    .import-success = ✅ <i>Успешно импотированно.</i>
    .export-plans_not_selected =  ❌ <i>Выберите хотя бы один план для экспорта.</i>
    .export-failed = ❌ <i>Не удалось экспортировать.</i>
    .export-success = ✅ <i>Выбранные планы экспортированы.</i>
    .trial-single-duration = ❌ <i>Пробный план может иметь только одну длительность.</i>
    .duration-already-exists = ❌ <i>Такая длительность уже существует.</i>
    .name-already-exists = ❌ <i>План с таким именем уже существует.</i>
    .user-already-allowed = ❌ <i>Индентификтор пользователя уже добавлен.</i>

    .updated = ✅ <i>План успешно обновлен.</i>
    .created = ✅ <i>План успешно создан.</i>
    .deleted = ✅ <i>План успешно удален.</i>

ntf-gateway =
    .not-configured = ❌ <i>Платежный шлюз не настроен.</i>
    .not-configurable = ❌ <i>У платежного шлюза отсутствуют настройки.</i>

    .test-payment-created = ✅ <i><a href="{ $url }">Тестовый платеж</a> успешно создан.</i>
    .test-payment-error = ❌ <i>Ошибка при создании тестового платежа.</i>
    .test-payment-confirmed = ✅ <i>Тестовый платеж успешно обработан.</i>

ntf-subscription =
    .plans-unavailable = ❌ <i>В данный момент нет доступных планов.</i>
    .gateways-unavailable = ❌ <i>В данный момент нет доступных платежных систем.</i>
    .renew-plan-unavailable = ❌ <i>Текущий план устарел и недоступен для продления.</i>
    .payment-creation-failed = ❌ <i>Ошибка при создании платежа. Попробуйте позже.</i>

ntf-broadcast =
    .message = { $content }
    .text-too-long = ❌ Превышено максимальное кол-во символов ({ $max_limit }).
    .list-empty = ❌ <i>Список рассылок пуст.</i>
    .plans-unavailable = ❌ <i>Нет доступных планов.</i>
    .audience-unavailable = ❌ <i>Нет пользователей для выбранной аудитории.</i>
    .content-empty = ❌ <i>Контент пуст.</i>
    .content-saved = ✅ <i>Контент успешно сохранен.</i>

    .not-cancelable = ❌ <i>Рассылку невозможно отменить.</i>
    .canceled = ✅ <i>Рассылка успешно отменена.</i>
    .deleting = ⚠️ <i>Выполняется удаление отправленных сообщений.</i>
    .already-deleted = ❌ <i>Рассылка уже удалена или находится в процессе удаления.</i>

    .deleted-success =
        ✅ Рассылка <code>{ $task_id }</code> успешно удалена.

        <blockquote>
        • <b>Всего сообщений</b>: { $total_count }
        • <b>Удалено</b>: { $deleted_count }
        • <b>Не удалось удалить</b>: { $failed_count }
        </blockquote>

ntf-importer =
    .not-file = ⚠️ <i>Отправьте базу данных в виде файла.</i>
    .db-failed = ❌ <i>Ошибка при экспорте пользователей из базы данных.</i>
    .users-empty = ❌ <i>Список пользователей в базе данных пуст.</i>

    .started = ✅ <i>Импорт запущен. Дождитесь завершения...</i>
    .already-running = ⚠️ <i>Импорт уже выполняется. Пожалуйста, подождите.</i>

ntf-sync =
    .started = ✅ <i>Синхронизация запущена. Дождитесь завершения...</i>
    .users-not-found = ❌ <i>Пользователи для синхронизации не найдены.</i>
    .already-running = ⚠️ <i>Синхронизация уже выполняется. Пожалуйста, подождите.</i>

ntf-menu-editor =
    .button-saved = ✅ <i>Кнопка успешно сохранена.</i>
    .invalid-payload = ❌ <i>Недопустимый формат URL для payload.</i>

ntf-devices =
    .deleted = ✅ <i>Устройство удалено.</i>
    .all-deleted = ✅ <i>Все устройства удалены.</i>
    .reissued = ✅ <i>Подписка успешно перевыпущена.</i>

email-otp =
    .title = Код подтверждения
    .message =
        Ваш код подтверждения: { $code }
        Код действует в течение 10 минут. Не передавайте его никому.

    .message-html =
        <p>Your verification code is:</p>
        <h2 style='letter-spacing:4px'>{ $code }</h2>
        <p>The code is valid for <strong>10 minutes</strong>. Do not share it with anyone.</p>

email-success-purchase =
    .title = Покупка успешно завершена
    .message =
        Ваш заказ успешно оформлен.
        Ссылка для подключения: { $subscription_url }
        Переходите в telegram-бота, для управления подпиской: { $bot_url }
        Спасибо за то что вы выбераете нас!

    .message-html =
        <!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KAGO VPN</title>
        <style>
        @media(max-width:600px){ sc-open }.wrap { sc-open } padding:16px 8px!important{ sc-close }.card{ sc-open }border-radius:12px!important;border-left:none!important;border-right:none!important;width:100%!important{ sc-close }.hd{ sc-open }padding:28px 20px 24px!important;border-radius:12px 12px 0 0!important{ sc-close }.hd h1{ sc-open }font-size:22px!important{ sc-close }.body,.btns,.stats,.foot{ sc-open }padding-left:20px!important;padding-right:20px!important{ sc-close }.btn{ sc-open }padding:14px!important;font-size:14px!important{ sc-close }.stat td{ sc-open }padding:12px 4px!important;font-size:12px!important{ sc-close }{ sc-close }
        </style>
        </head><body style="margin:0;padding:0;background:#EEF3FB;font-family:Arial,sans-serif;">
        <div style="display:none;">Ваша подписка KAGO VPN активирована. Подключитесь за 2 шага.</div>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#16A34A;">&#9679; Подписка активна</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">Добро пожаловать,<br><span style="color:#3B6FD4;">вы защищены!</span></h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">Ваша подписка успешно оформлена. Выполните два шага, чтобы начать.</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;">
        <p style="margin:0 0 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94A3B8;">Что нужно сделать</p>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#3B6FD4;border-radius:50%;text-align:center;line-height:30px;font-size:13px;font-weight:800;color:#fff;">1</div></td><td style="padding-left:12px;"><b style="font-size:14px;color:#1e2a4a;">Подключите VPN</b><br><span style="font-size:13px;color:#64748B;">Нажмите кнопку ниже — конфигурация загрузится автоматически</span></td></tr></table>
        <div style="width:1px;height:10px;background:#E2E8F0;margin:6px 0 6px 14px;"></div>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#F1F5F9;border:1.5px solid #E2E8F0;border-radius:50%;text-align:center;line-height:27px;font-size:13px;font-weight:800;color:#94A3B8;">2</div></td><td style="padding-left:12px;"><b style="font-size:14px;color:#1e2a4a;">Откройте Telegram</b><br><span style="font-size:13px;color:#64748B;">После подключения перейдите в бот для управления подпиской</span></td></tr></table>
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $subscription_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;margin-bottom:8px;">&#9889; Подключить VPN</a>
          <a href="{ $bot_url }" class="btn" style="display:block;padding:13px;background:#F8FAFF;border:1.5px solid #BFDBFE;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:600;color:#3B6FD4;">&#9992;&#65039; Открыть Telegram</a>
        </td></tr>
        <tr><td style="padding:0 32px;"><div style="height:1px;background:#EEF2FF;"></div></td></tr>
        <tr><td class="stats" style="padding:20px 32px;"><table class="stat" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #E2E8F0;border-radius:12px;overflow:hidden;"><tr>
          <td align="center" style="background:#F8FAFF;padding:16px 8px;width:33%;"><b style="font-size:14px;color:#1e2a4a;display:block;">{ $expire_date }</b><span style="font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#94A3B8;">Окончание</span></td>
          <td align="center" style="background:#F8FAFF;padding:16px 8px;width:34%;border-left:1px solid #E2E8F0;border-right:1px solid #E2E8F0;"><b style="font-size:14px;color:#1e2a4a;display:block;">{ $devices }</b><span style="font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#94A3B8;">Лимит</span></td>
          <td align="center" style="background:#F8FAFF;padding:16px 8px;width:33%;"><b style="font-size:14px;color:#1e2a4a;display:block;">{ $plan_name }</b><span style="font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#94A3B8;">Тариф</span></td>
        </tr></table></td></tr>
        <tr><td class="foot" align="center" style="background:#F8FAFF;border-top:1px solid #EEF2FF;padding:20px 32px;border-radius:0 0 16px 16px;">
          <p style="margin:0 0 10px;font-size:12px;"><a href="https://usekago.net/help" style="color:#94A3B8;text-decoration:none;margin:0 8px;">Поддержка</a><a href="https://usekago.net/faq" style="color:#94A3B8;text-decoration:none;margin:0 8px;">FAQ</a><a href="https://usekago.net/terms" style="color:#94A3B8;text-decoration:none;margin:0 8px;">Условия</a></p>
          <p style="margin:0;font-size:11px;color:#CBD5E1;line-height:1.7;">© 2026 KAGO VPN · Письмо отправлено автоматически. Не отвечайте на него.</p>
        </td></tr>
        </table></td></tr></table></body></html>

