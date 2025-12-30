ntf-error-lost-context = <i>⚠️ Произошла ошибка. Диалог перезапущен.</i>
ntf-error-log-not-found = <i>⚠️ Ошибка: Лог файл не найден.</i>

ntf-command-paysupport = 💸 <b>Чтобы запросить возврат, обратитесь в нашу службу поддержки.</b>
ntf-command-help = 🆘 <b>Нажмите кнопку ниже, чтобы связаться с поддержкой. Мы поможем решить вашу проблему.</b>
ntf-channel-join-required = ❇️ Подпишитесь на наш канал и получайте <b>бесплатные дни, акции и новости</b>! После подписки нажмите кнопку «Подтвердить».
ntf-channel-join-required-left = ⚠️ Вы отписались от нашего канала! Подпишитесь, чтобы иметь возможность пользоваться ботом.
ntf-rules-accept-required = ⚠️ <b>Перед использованием сервиса, пожалуйста, ознакомьтесь и примите <a href="{ $url }">Условия использования</a> сервиса.</b>

ntf-double-click-confirm = <i>⚠️ Нажмите еще раз, чтобы подтвердить действие.</i>
ntf-channel-join-error = <i>⚠️ Мы не видим вашу подписку на канал. Проверьте, что вы подписались, и попробуйте еще раз.</i>
ntf-throttling-many-requests = <i>⚠️ Вы отправляете слишком много запросов, пожалуйста, подождите немного.</i>
ntf-squads-empty = <i>⚠️ Сквады не найдены. Проверьте их наличие в панели.</i>
ntf-invite-withdraw-points-error = ❌ У вас недостаточно баллов для выполнения обмена.

ntf-connect-not-available =
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
    [0] Срок действия вашей подписки истек. Чтобы продолжить пользоваться сервисом, продлите подписку или оформите новую.
    *[1] Ваш бесплатный пробный период закончился. Оформите подписку, чтобы продолжить пользоваться сервисом!
    }
    *[OTHER] Произошла ошибка при проверке статуса или ваша подписка была отключена. Обратитесь в поддержку.
    }

ntf-user-not-found = <i>❌ Пользователь не найден.</i>
ntf-user-transactions-empty = <i>❌ Список транзакций пуст.</i>
ntf-user-subscription-empty = <i>❌ Текущая подписка не найдена.</i>
ntf-user-plans-empty = <i>❌ Нет доступных планов для выдачи.</i>
ntf-user-devices-empty = <i>❌ Список устройств пуст.</i>
ntf-user-invalid-number = <i>❌ Некорректное число.</i>
ntf-user-allowed-plans-empty = <i>❌ Нет доступных планов для предоставления доступа.</i>
ntf-user-message-success = <i>✅ Сообщение успешно отправлено.</i>
ntf-user-message-not-sent = <i>❌ Не удалось отправить сообщение.</i>
ntf-user-sync-already = <i>✅ Данные подписки совпадают.</i>
ntf-user-sync-missing-data = <i>⚠️ Синхронизация невозможна. Данные подписки отсутствуют и на панели, и в боте.</i>
ntf-user-sync-success = <i>✅ Синхронизация подписки выполнена.</i>

ntf-user-invalid-expire-time = <i>❌ Невозможно { $operation ->
    [ADD] продлить подписку на указанное количество дней
    *[SUB] уменьшить срок подписки на указанное количество дней
    }.</i>

ntf-user-invalid-points = <i>❌ Невозможно { $operation ->
    [ADD] добавить указанное количество баллов
    *[SUB] отнять указанное количество баллов
    }.</i>

ntf-referral-invalid-reward = <i>❌ Некорректное значение.</i>

ntf-access-denied = <i>🚧 Бот в режиме обслуживания, попробуйте позже.</i>
ntf-access-denied-registration = <i>❌ Регистрация новых пользователей отключена.</i>
ntf-access-denied-only-invited = <i>❌ Регистрация новых пользователей доступна только через приглашение другим пользователем.</i>
ntf-access-denied-purchasing = <i>🚧 Бот в режиме обслуживания, Вам придет уведомление когда бот снова будет доступен.</i>
ntf-access-allowed = <i>❇️ Весь функционал бота снова доступен, спасибо за ожидание.</i>
ntf-access-id-saved = <i>✅ ID канала/группы успешно обновлен.</i>
ntf-access-link-saved = <i>✅ Ссылка на канал/группу успешно обновлена.</i>
ntf-access-channel-invalid = <i>❌ Некорректная ссылка или ID канала/группы.</i>

ntf-plan-invalid-name = <i>❌ Некорректное имя.</i>
ntf-plan-invalid-description = <i>❌ Некорректное описание.</i>
ntf-plan-invalid-tag = <i>❌ Некорректный тег.</i>
ntf-plan-invalid-number = <i>❌ Некорректное число.</i>
ntf-plan-trial-once-duration = <i>❌ Пробный план может иметь только одну длительность.</i>
ntf-plan-trial-already-exists = <i>❌ Пробный план уже существует.</i>
ntf-plan-duration-already-exists = <i>❌ Такая длительность уже существует.</i>
ntf-plan-duration-last = <i>❌ Нельзя удалить последнюю длительность.</i>
ntf-plan-save-error = <i>❌ Ошибка сохранения плана.</i>
ntf-plan-name-already-exists = <i>❌ План с таким именем уже существует.</i>
ntf-plan-invalid-user-id = <i>❌ Некорректный ID пользователя.</i>
ntf-plan-no-user-found = <i>❌ Пользователь не найден.</i>
ntf-plan-user-already-allowed = <i>❌ Пользователь уже добавлен в список разрешенных.</i>
ntf-plan-confirm-delete = <i>⚠️ Нажмите еще раз, чтобы удалить.</i>
ntf-plan-updated-success = <i>✅ План успешно обновлен.</i>
ntf-plan-created-success = <i>✅ План успешно создан.</i>
ntf-plan-deleted-success = <i>✅ План успешно удален.</i>
ntf-plan-internal-squads-empty = <i>❌ Выберите хотя бы один внутренний сквад.</i>

ntf-gateway-not-configured = <i>❌ Платежный шлюз не настроен.</i>
ntf-gateway-not-configurable = <i>❌ Платежный шлюз не имеет настроек.</i>
ntf-gateway-field-wrong-value = <i>❌ Некорректное значение.</i>
ntf-gateway-test-payment-created = <i>✅ <a href="{ $url }">Тестовый платеж</a> успешно создан.</i>
ntf-gateway-test-payment-error = <i>❌ Произошла ошибка при создании тестового платежа.</i>
ntf-gateway-test-payment-confirmed = <i>✅ Тестовый платеж успешно обработан.</i>

ntf-subscription-plans-not-available = <i>❌ Нет доступных планов.</i>
ntf-subscription-gateways-not-available = <i>❌ Нет доступных платежных систем.</i>
ntf-subscription-renew-plan-unavailable = <i>❌ Ваш план устарел и не доступен для продления.</i>
ntf-subscription-payment-creation-failed = <i>❌ Произошла ошибка при создании платежа, попробуйте позже.</i>

ntf-broadcast-list-empty = <i>❌ Список рассылок пуст.</i>
ntf-broadcast-audience-not-available = <i>❌ Нет доступных пользователей для выбранной аудитории.</i>
ntf-broadcast-audience-not-active = <i>❌ Нет пользователей у которых есть АКТИВНАЯ подписка с данным планом.</i>
ntf-broadcast-plans-not-available = <i>❌ Нет доступных планов.</i>
ntf-broadcast-empty-content = <i>❌ Контент пустой.</i>
ntf-broadcast-wrong-content = <i>❌ Некорректный контент.</i>
ntf-broadcast-content-saved = <i>✅ Контент сообщения успешно сохранен.</i>
ntf-broadcast-preview = { $content }
ntf-broadcast-not-cancelable = <i>❌ Рассылка не может быть отменена.</i>
ntf-broadcast-canceled = <i>✅ Рассылка успешно отменена.</i>
ntf-broadcast-deleting = <i>⚠️ Идет удаление всех отправленных сообщений.</i>
ntf-broadcast-already-deleted = <i>❌ Рассылка находится в процессе удаления или уже удалена.</i>

ntf-broadcast-deleted-success =
    ✅ Рассылка <code>{ $task_id }</code> успешно удалена.

    <blockquote>
    • <b>Всего сообщений</b>: { $total_count }
    • <b>Успешно удалено</b>: { $deleted_count }
    • <b>Не удалось удалить</b>: { $failed_count }
    </blockquote>

ntf-trial-unavailable = <i>❌ Пробная подписка временно недоступна.</i>

ntf-importer-not-file = <i>⚠️ Отправьте базу данных в виде файла.</i>
ntf-importer-db-invalid = <i>❌ Этот файл не может быть импортирован.</i>
ntf-importer-db-failed = <i>❌ Ошибка при импорте базы данных.</i>
ntf-importer-exported-users-empty =  <i>❌ Список пользователей в базе данных пуст.</i>
ntf-importer-internal-squads-empty = <i>❌ Выберите хотя бы один внутренний сквад.</i>
ntf-importer-import-started = <i>✅ Импорт пользователей запущен, ожидайте...</i>
ntf-importer-sync-started = <i>✅ Синхронизация пользователей запущена, ожидайте...</i>
ntf-importer-users-not-found = <i>❌ Не удалось найти пользователей для синхронизации.</i>
ntf-importer-not-support = <i>⚠️ Импорт всех данных из 3xui-shop временно недоступен. Вы можете воспользоваться импортом из панели 3X-UI!</i>
ntf-importer-sync-already-running = <i>⚠️ Синхронизация пользователей уже была запущена, ожидайте...</i>