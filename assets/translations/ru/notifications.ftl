ntf-error =
    .unknown = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Произошла ошибка.</i>
    .permission-denied = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>У вас недостаточно прав.</i>
    .log-not-found = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Лог файл не найден.</i>
    .logs-disabled = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Логирование в файл отключено.</i>
    
    .lost-context = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Произошла ошибка. Перезапустите диалог командой /start.</i>
    .lost-context-restart = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Произошла ошибка. Диалог перезапущен.</i>

ntf-common =
    .trial-unavailable = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Пробная подписка временно недоступна.</i>
    .throttling = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Вы отправляете слишком много запросов. Пожалуйста, подождите.</i>
    .double-click-confirm = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Нажмите еще раз, чтобы подтвердить действие.</i>
    .squads-empty = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Сквады не найдены. Проверьте их наличие в панели.</i>

    .withdraw-points = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>У вас недостаточно баллов для выполнения обмена.</i>
    .internal-squads-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Выберите хотя бы один внутренний сквад.</i>

    .invalid-value = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Некорректное значение.</i>
    .value-updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Параметр успешно обновлен.</i>
    .cooldown-active = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> <i>Временно недоступно. Попробуйте снова через { $available_at }.</i>

    .plan-not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>План не найден или недоступен.</i>
    .connect-not-available =
    <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> { $status ->
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
    .paysupport = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> <b>Чтобы запросить возврат, обратитесь в службу поддержки.</b>
    .rules = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <b>Пожалуйста, ознакомьтесь с <a href="{ $url }">Условиями использования</a> перед использованием сервиса.</b>
    .help = <tg-emoji emoji-id="6032636795387121097">🆘</tg-emoji> <b>Нажмите кнопку ниже, чтобы связаться с поддержкой.</b>

ntf-requirement =
    .channel-join-required = ❇️ Подпишитесь на наш канал и получайте <b>бесплатные дни, акции и новости</b>. После подписки нажмите «Подтвердить».
    .channel-join-required-left = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Вы отписались от канала. Подпишитесь, чтобы продолжить пользоваться ботом.
    .rules-accept-required = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <b>Перед использованием сервиса ознакомьтесь и примите <a href="{ $url }">Условия использования</a>.</b>
    .channel-join-error = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Мы не видим вашу подписку на канал. Проверьте подписку и попробуйте снова.
    .trial-paused = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Пробный период приостановлен — вы отписались от канала. Подпишитесь снова, чтобы возобновить доступ.
    .trial-restored = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Пробный период возобновлен.
    
ntf-user =
    .email-purchase-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Письмо о покупке успешно отправлено.</i>
    .email-purchase-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Не удалось отправить письмо о покупке.</i>
    .email-connect-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Письмо с приглашением в Telegram успешно отправлено.</i>
    .email-connect-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Не удалось отправить письмо с приглашением в Telegram.</i>
    .email-custom-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Произвольное письмо успешно отправлено.</i>
    .email-custom-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Не удалось отправить произвольное письмо.</i>
    .email-custom-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Текст письма не задан.</i>
    .email-custom-no-email = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>У пользователя не задана почта.</i>
    .email-custom-preview =
        <tg-emoji emoji-id="6039573425268201570">📨</tg-emoji> <b>Предпросмотр письма</b>

        { $body }
    .email-set-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Почта пользователя обновлена.</i>
    .email-cleared = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Почта пользователя удалена.</i>
    .email-duplicate = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Эта почта уже используется другим пользователем.</i>
    .email-required = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Нельзя удалить почту: у пользователя нет Telegram ID.</i>
    .password-reset-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Пароль пользователя обновлён. Активные сессии завершены.</i>
    .password-reset-invalid = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Пароль должен быть от 8 до 256 символов.</i>
    .password-reset-no-email = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>У пользователя не задана почта — пароль не используется.</i>
    .not-found = <i><tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Пользователь не найден.</i>
    .transaction-not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Транзакция не найдена.</i>
    .transactions-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Список транзакций пуст.</i>
    .subscription-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Активная подписка не найдена.</i>
    .subscription-deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Подписка успешно удалена.</i>
    .plans-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Нет доступных планов.</i>
    .devices-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Список устройств пуст.</i>
    .allowed-plans-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Нет доступных планов для предоставления доступа.</i>
    .referral-reset = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Реферальная ссылка успешно сброшена.</i>
    .message-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Сообщение успешно отправлено.</i>
    .message-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Не удалось отправить сообщение.</i>

    .sync-already = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Данные подписки идентичны.</i>
    .sync-missing-data = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Синхронизация невозможна. Данные подписки отсутствуют в панели и в боте.</i>
    .sync-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Синхронизация подписки выполнена.</i>

    .invalid-expire-time = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Невозможно { $operation ->
    [ADD] продлить
    *[SUB] сократить
    } срок подписки на указанное количество дней.</i>

    .invalid-points = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Невозможно { $operation ->
    [ADD] добавить
    *[SUB] списать
    } указанное количество баллов.</i>

ntf-access =
    .maintenance = 🚧 <i>Бот находится на обслуживании. Попробуйте позже.</i>
    .registration-disabled = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Регистрация новых пользователей отключена.</i>
    .registration-invite-only = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Регистрация доступна только по приглашению.</i>
    .payments-disabled = 🚧 <i>Платежи временно недоступны! Вы получите уведомление после восстановления.</i>
    .payments-restored = ❇️ <i>Платежи восстановлены! Теперь вы можете купить или продлить подписку. Спасибо за ожидание.</i>

ntf-plan =
    .not-file = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Отправьте планы в виде json файла.</i>
    .import-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Не удалось импортировать.</i>
    .import-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Успешно импортировано.</i>
    .export-plans-not-selected = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Выберите хотя бы один план для экспорта.</i>
    .export-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Не удалось экспортировать.</i>
    .export-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Выбранные планы экспортированы.</i>
    .trial-single-duration = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Пробный план может иметь только одну длительность.</i>
    .duration-already-exists = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Такая длительность уже существует.</i>
    .name-already-exists = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>План с таким именем уже существует.</i>
    .user-already-allowed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Идентификатор пользователя уже добавлен.</i>

    .updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>План успешно обновлен.</i>
    .created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>План успешно создан.</i>
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>План успешно удален.</i>

ntf-gateway =
    .not-configured = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Платежный шлюз не настроен.</i>
    .not-configurable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>У платежного шлюза отсутствуют настройки.</i>
    .test-payment-created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i><a href="{ $url }">Тестовый платеж</a> успешно создан.</i>
    .test-payment-error = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Ошибка при создании тестового платежа.</i>
    .test-payment-confirmed = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Тестовый платеж успешно обработан.</i>
    .field-reset = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Значение поля очищено.</i>
    .field-reset-deactivated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Значение поля очищено. Шлюз отключён: не хватает обязательных настроек.</i>

ntf-subscription =
    .plans-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>В данный момент нет доступных планов.</i>
    .gateways-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>В данный момент нет доступных платежных систем.</i>
    .renew-plan-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Текущий план устарел и недоступен для продления.</i> Нажите на кнопку <b>"Измененить"</b>.
    .payment-creation-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Ошибка при создании платежа. Попробуйте позже.</i>

ntf-broadcast =
    .text-too-long = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Превышено максимальное кол-во символов ({ $max_limit }).
    .list-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Список рассылок пуст.</i>
    .plans-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Нет доступных планов.</i>
    .audience-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Нет пользователей для выбранной аудитории.</i>
    .content-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Контент пуст.</i>
    .content-saved = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Контент успешно сохранен.</i>

    .not-cancelable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Рассылку невозможно отменить.</i>
    .canceled = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Рассылка успешно отменена.</i>
    .deleting = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Выполняется удаление отправленных сообщений.</i>
    .already-deleted = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Рассылка уже удалена или находится в процессе удаления.</i>

    .deleted-success =
        ℹ️ Результат удаления рассылки <code>{ $task_id }</code>.

        <blockquote>
        • <b>Всего сообщений</b>: { $total_count }
        • <b>Удалено</b>: { $deleted_count }
        • <b>Не удалось удалить</b>: { $failed_count }
        </blockquote>

ntf-importer =
    .not-file = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Отправьте базу данных в виде файла.</i>
    .db-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Ошибка при экспорте пользователей из базы данных.</i>
    .users-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Список пользователей в базе данных пуст.</i>

    .started = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Импорт запущен. Дождитесь завершения...</i>
    .already-running = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Импорт уже выполняется. Пожалуйста, подождите.</i>

ntf-sync =
    .from-panel-started = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Синхронизация панель → бот запущена. Дождитесь завершения...</i>
    .from-bot-started = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Синхронизация бот → панель запущена. Дождитесь завершения...</i>
    .users-not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Пользователи для синхронизации не найдены.</i>
    .already-running = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Синхронизация уже выполняется. Пожалуйста, подождите.</i>

ntf-menu-editor =
    .button-saved = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Кнопка успешно сохранена.</i>
    .invalid-payload = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Недопустимый формат URL.</i>

ntf-devices =
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Устройство удалено.</i>
    .all-deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Все устройства удалены.</i>
    .reissued = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Подписка успешно перевыпущена.</i>

ntf-backup =
    .assets-started = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> <i>Создание бэкапа ассетов...</i>
    .db-started = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> <i>Создание бэкапа базы данных...</i>
    .error = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Ошибка при создании бэкапа</i>

ntf-blacklist =
    .list-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Список заблокированных пуст.</i>
    .no-ids-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>По ссылке не найдено ни одного ID.</i>
    .source-removed = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Список удален.</i>
    .blocked-ids-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Список заблокированных ID пуст.</i>
    .blocked-ids-cleared = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Очищено { $count } ID.</i>
    
    .block-result =
    ℹ️ Результат блокировки.

    <blockquote>
    • <b>Всего ID</b>: { $total }
    • <b>Заблокировано пользователей</b>: { $blocked_users }
    • <b>Заблокировано ID</b>: { $blocked_ids }
    • <b>Уже заблокированные</b>: { $already_blocked }
    </blockquote>

ntf-invite =
    .referral-reset = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Реферальная ссылка обновлена.</i>

ntf-promocode =
    .not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Промокод не найден или недействителен.</i>
    .not-available = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Промокод недоступен.</i>
    .expired = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Срок действия промокода истек.</i>
    .already-activated = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Вы уже активировали данный промокод.</i>
    .activated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Промокод успешно активирован!</i>
    .activation-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Не удалось активировать промокод. Попробуйте позже.</i>
    .code-exists = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Промокод с таким кодом уже существует.</i>
    .created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Промокод создан.</i>
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Промокод удален.</i>
    .fields-required = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Заполните значение награды.</i>
    .invalid-code = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Код может содержать только латинские буквы, цифры, дефис и подчёркивание.</i>
    .plans-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Нет доступных планов.</i>
    .updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Промокод обновлен.</i>

ntf-ad-link =
    .created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Рекламная ссылка создана.</i>
    .updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Рекламная ссылка обновлена.</i>
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Рекламная ссылка удалена.</i>

sc-open = { "{" }
sc-close = { "}" }

hdr-email-html =
    <!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KAGO VPN</title>
    <style>
    @media(max-width:600px){ sc-open }.wrap{ sc-open }padding:16px 8px!important{ sc-close }.card{ sc-open }border-radius:12px!important;border-left:none!important;border-right:none!important;width:100%!important{ sc-close }.hd{ sc-open }padding:28px 20px 24px!important;border-radius:12px 12px 0 0!important{ sc-close }.hd h1{ sc-open }font-size:22px!important{ sc-close }.body,.btns,.foot{ sc-open }padding-left:20px!important;padding-right:20px!important{ sc-close }.btn{ sc-open }padding:14px!important;font-size:14px!important{ sc-close }{ sc-close }
    </style>
    </head><body style="margin:0;padding:0;background:#EEF3FB;font-family:Arial,sans-serif;">

ftr-email-html =
    <tr><td class="foot" align="center" style="background:#F8FAFF;border-top:1px solid #EEF2FF;padding:20px 32px;border-radius:0 0 16px 16px;">
      <p style="margin:0 0 10px;font-size:12px;"><a href="https://usekago.net/help" style="color:#94A3B8;text-decoration:none;margin:0 8px;">Поддержка</a><a href="https://usekago.net/faq" style="color:#94A3B8;text-decoration:none;margin:0 8px;">FAQ</a><a href="https://usekago.net/terms" style="color:#94A3B8;text-decoration:none;margin:0 8px;">Условия</a></p>
      <p style="margin:0;font-size:11px;color:#CBD5E1;line-height:1.7;">© 2026 KAGO VPN · Письмо отправлено автоматически. Не отвечайте на него.</p>
    </td></tr>
    </table></td></tr></table></body></html>

email-success-purchase =
    .title = { $purchase_type ->
        [RENEW] Подписка успешно продлена
        [CHANGE] Тариф успешно изменён
       *[NEW] Покупка успешно завершена
        }
    .message =
        { $purchase_type ->
            [RENEW] Ваша подписка успешно продлена.
            [CHANGE] Ваш тариф успешно изменён.
           *[NEW] Ваш заказ успешно оформлен.
        }
        Ссылка для подключения: { $subscription_url }
        Переходите в telegram-бота, для управления подпиской: { $bot_url }
        Спасибо за то что вы выбераете нас!

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">{ $purchase_type ->
            [RENEW] Ваша подписка KAGO VPN продлена. Можно продолжать пользоваться сервисом.
            [CHANGE] Ваш тариф KAGO VPN обновлён. Подключитесь заново, чтобы применить изменения.
           *[NEW] Ваша подписка KAGO VPN активирована. Подключитесь за 2 шага и начните пользоваться.
        }</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#16A34A;">&#9679; { $purchase_type ->
            [RENEW] Подписка продлена
            [CHANGE] Тариф изменён
           *[NEW] Подписка активна
        }</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">{ $purchase_type ->
            [RENEW] С возвращением,<br><span style="color:#3B6FD4;">подписка продлена!</span>
            [CHANGE] Тариф обновлён,<br><span style="color:#3B6FD4;">всё готово!</span>
           *[NEW] Добро пожаловать,<br><span style="color:#3B6FD4;">вы защищены!</span>
        }</h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">{ $purchase_type ->
            [RENEW] Ваша подписка успешно продлена. Можно продолжать пользоваться сервисом.
            [CHANGE] Ваш тариф успешно изменён. Подключитесь заново, чтобы применить изменения.
           *[NEW] Ваша подписка успешно оформлена. Выполните два шага, чтобы начать.
        }</p>
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
        { ftr-email-html }

email-failed-purchase =
    .title = Платёж не прошёл
    .message =
        К сожалению, ваш платёж не был обработан.

        Попробуйте повторить попытку или обратитесь в поддержку.
        Перейти в бот: { $bot_url }

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">Ваш платёж не прошёл — попробуйте повторить или свяжитесь с поддержкой, мы поможем разобраться.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#FFF5F5;border-bottom:1px solid #FED7D7;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#FFF5F5;border:1px solid #FED7D7;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#C53030;">&#9888; Платёж не прошёл</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">Что-то пошло не так</h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">К сожалению, ваш платёж не был обработан. Попробуйте ещё раз — это займёт пару секунд.</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;">
        <p style="margin:0 0 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94A3B8;">Что делать дальше</p>
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#3B6FD4;border-radius:50%;text-align:center;line-height:30px;font-size:13px;font-weight:800;color:#fff;">1</div></td><td style="padding-left:12px;padding-bottom:12px;"><b style="font-size:14px;color:#1e2a4a;">Перейдите в бот</b><br><span style="font-size:13px;color:#64748B;">Откройте Telegram и попробуйте оплатить снова</span></td></tr>
        <tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#F1F5F9;border:1.5px solid #E2E8F0;border-radius:50%;text-align:center;line-height:27px;font-size:13px;font-weight:800;color:#94A3B8;">2</div></td><td style="padding-left:12px;"><b style="font-size:14px;color:#1e2a4a;">Свяжитесь с поддержкой</b><br><span style="font-size:13px;color:#64748B;">Если проблема повторяется — мы поможем разобраться</span></td></tr>
        </table>
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $bot_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;">&#9992;&#65039; Перейти в бот</a>
        </td></tr>
        { ftr-email-html }

email-custom-message =
    .title = Сообщение от KAGO VPN
    .message =
        { $body }

        Открыть Telegram-бота: { $bot_url }

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">У вас новое сообщение от KAGO VPN — откройте письмо, чтобы узнать подробности.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#3B6FD4;">&#9993; Сообщение</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">У нас для вас<br><span style="color:#3B6FD4;">важное сообщение</span></h1>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;font-size:15px;color:#1e2a4a;line-height:1.6;">
          { $body }
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $bot_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;">&#9992;&#65039; Открыть Telegram</a>
        </td></tr>
        { ftr-email-html }

email-notification =
    .title = Уведомление от KAGO VPN
    .message =
        { $body }

        Подключите Telegram-бота для управления подпиской: { $bot_url }

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">У вас новое уведомление о вашей подписке KAGO VPN — проверьте детали прямо сейчас.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#3B6FD4;">&#128276; Уведомление</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">Новое уведомление<br><span style="color:#3B6FD4;">от KAGO VPN</span></h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">Подключите Telegram-бота, чтобы получать уведомления мгновенно и управлять подпиской в пару кликов.</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;font-size:15px;color:#1e2a4a;line-height:1.6;">
          { $body }
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $bot_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;">&#9992;&#65039; Подключить Telegram</a>
          <a href="https://usekago.net/plans" class="btn" style="display:block;margin-top:10px;padding:15px;background:#fff;border:1px solid #3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#3B6FD4;">&#127760; На сайт</a>
        </td></tr>
        { ftr-email-html }

email-verification =
    .title = Ваш код подтверждения — { $code }
    .message =
        Ваш код подтверждения: { $code }

        Он действителен { $minutes } минут. Если вы не запрашивали код — просто проигнорируйте это письмо.

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">Ваш код подтверждения KAGO VPN: { $code }. Он действителен { $minutes } минут.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#3B6FD4;">&#128274; Подтверждение почты</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">Ваш код<br><span style="color:#3B6FD4;">подтверждения</span></h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">Введите этот код, чтобы подтвердить адрес электронной почты.</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;">
        <div style="background:#F8FAFF;border:1px solid #DBEAFE;border-radius:12px;padding:24px;text-align:center;">
          <p style="margin:0 0 10px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94A3B8;">Код подтверждения</p>
          <div style="font-size:38px;font-weight:800;letter-spacing:.32em;color:#1e2a4a;font-family:'Courier New',Courier,monospace;">{ $code }</div>
        </div>
        <p style="margin:18px 0 0;font-size:13px;color:#64748B;line-height:1.6;text-align:center;">&#9201; Код действителен <b style="color:#1e2a4a;">{ $minutes } минут</b>. Никому его не сообщайте.</p>
        </td></tr>
        <tr><td style="padding:0 32px;"><div style="height:1px;background:#EEF2FF;"></div></td></tr>
        <tr><td style="padding:20px 32px 8px;"><p style="margin:0;font-size:12px;color:#94A3B8;line-height:1.6;">Если вы не запрашивали этот код, просто проигнорируйте письмо — с вашим аккаунтом ничего не произойдёт.</p></td></tr>
        { ftr-email-html }
