ntf-error =
    .unknown = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>An error occurred.</i>
    .permission-denied = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>You do not have sufficient permissions.</i>
    .log-not-found = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Log file not found.</i>
    .logs-disabled = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>File logging is disabled.</i>
    
    .lost-context = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>An error occurred. Restart the dialog with the /start command.</i>
    .lost-context-restart = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>An error occurred. The dialog has been restarted.</i>

ntf-common =
    .trial-unavailable = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Trial subscription is temporarily unavailable.</i>
    .throttling = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>You are sending too many requests. Please wait.</i>
    .double-click-confirm = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Press again to confirm the action.</i>
    .squads-empty = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Squads not found. Check that they exist in the panel.</i>

    .withdraw-points = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>You do not have enough points to make the exchange.</i>
    .internal-squads-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Select at least one internal squad.</i>

    .invalid-value = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Invalid value.</i>
    .value-updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Setting updated successfully.</i>
    .cooldown-active = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> <i>Temporarily unavailable. Try again in { $available_at }.</i>

    .plan-not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Plan not found or unavailable.</i>
    .devices-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Device management is unavailable: no active subscription with a device limit.</i>
    .payment-processing = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> <i>Your payment is still being processed. We will notify you as soon as it is credited.</i>
    .connect-not-available =
    ⚠️ { $status ->
    [LIMITED]
    You have used up all of your available traffic. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Renew your subscription to reset your traffic and keep using the service!
        *[RESET] Your traffic will be restored in { $reset_time }. You can also renew your subscription to reset it.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Get a subscription to keep using the service!
        *[RESET] Your traffic will be restored in { $reset_time }. You can also get a subscription to use the service without limits.
        }
    }
    [EXPIRED]  
    { $is_trial ->
    [0] Your subscription has expired. Renew it or get a new one.
    *[1] The free trial has ended. Get a subscription to keep using the service.
    }
    *[OTHER] An error occurred while checking the status, or the subscription was disabled. Contact support.
    }
    
ntf-command =
    .paysupport = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> <b>To request a refund, contact support.</b>
    .rules = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <b>Please read the <a href="{ $url }">Terms of Use</a> before using the service.</b>
    .help = <tg-emoji emoji-id="6032636795387121097">🆘</tg-emoji> <b>Press the button below to contact support.</b>

ntf-requirement =
    .channel-join-required = ❇️ Subscribe to our channel and get <b>free days, promotions and news</b>. After subscribing, press "Confirm".
    .channel-join-required-left = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> You have unsubscribed from the channel. Subscribe to keep using the bot.
    .rules-accept-required = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <b>Before using the service, read and accept the <a href="{ $url }">Terms of Use</a>.</b>
    .channel-join-error = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> We can't see your channel subscription. Check your subscription and try again.
    .trial-paused = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Your trial is paused — you unsubscribed from the channel. Subscribe again to restore access.
    .trial-restored = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Your trial has been resumed.
    
ntf-user =
    .email-purchase-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Purchase email sent successfully.</i>
    .email-purchase-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Failed to send the purchase email.</i>
    .email-connect-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Telegram invitation email sent successfully.</i>
    .email-connect-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Failed to send the Telegram invitation email.</i>
    .email-custom-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Custom email sent successfully.</i>
    .email-custom-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Failed to send the custom email.</i>
    .email-custom-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Email text is not set.</i>
    .email-custom-no-email = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The user has no email set.</i>
    .email-custom-preview =
        <tg-emoji emoji-id="6039573425268201570">📨</tg-emoji> <b>Email preview</b>

        { $body }
    .email-set-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>User email updated.</i>
    .email-cleared = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>User email deleted.</i>
    .email-duplicate = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>This email is already used by another user.</i>
    .email-required = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Cannot delete the email: the user has no Telegram ID.</i>
    .password-reset-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>User password updated. Active sessions have been terminated.</i>
    .password-reset-invalid = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The password must be between 8 and 256 characters.</i>
    .password-reset-no-email = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The user has no email set — the password is not used.</i>
    .not-found = <i><tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> User not found.</i>
    .transaction-not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Transaction not found.</i>
    .transactions-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The transaction list is empty.</i>
    .subscription-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Active subscription not found.</i>
    .subscription-deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Subscription deleted successfully.</i>
    .plans-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No plans available.</i>
    .devices-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The device list is empty.</i>
    .allowed-plans-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No plans available to grant access to.</i>
    .referral-reset = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Referral link reset successfully.</i>
    .message-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Message sent successfully.</i>
    .message-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Failed to send the message.</i>

    .sync-already = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Subscription data is identical.</i>
    .sync-missing-data = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Synchronization is not possible. Subscription data is missing from both the panel and the bot.</i>
    .sync-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Subscription synchronized.</i>

    .invalid-expire-time = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Unable to { $operation ->
    [ADD] extend
    *[SUB] shorten
    } the subscription by the specified number of days.</i>

    .invalid-points = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Unable to { $operation ->
    [ADD] add
    *[SUB] deduct
    } the specified number of points.</i>

ntf-access =
    .maintenance = 🚧 <i>The bot is under maintenance. Try again later.</i>
    .registration-disabled = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Registration of new users is disabled.</i>
    .registration-invite-only = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Registration is available by invitation only.</i>
    .payments-disabled = 🚧 <i>Payments are temporarily unavailable! You will be notified once they are restored.</i>
    .payments-restored = ❇️ <i>Payments are restored! You can now buy or renew a subscription. Thanks for waiting.</i>

ntf-auth =
    .login-code = <tg-emoji emoji-id="5280607998353334776">🔐</tg-emoji> <b>Web account login code: <code>{ $code }</code></b>
        <blockquote><i>The code is valid for { $minutes } minutes. If you did not request a login, ignore this message.</i></blockquote>{ $has_link ->
            [yes] { "" }
                <a href="{ $link }">🔗 Log in with one tap</a>
           *[other] { "" }
        }

ntf-profile =
    .email-invalid = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Invalid email.</i>
    .email-same = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>This email is already linked and confirmed.</i>
    .email-duplicate = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>This email is already used by another user.</i>
    .email-cooldown = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Please wait before requesting the code again.</i>
    .email-disabled = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Email sending is not configured.</i>
    .email-send-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Failed to send the code. Try again later.</i>
    .email-code-sent = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Confirmation code sent to your email.</i>
    .email-code-invalid = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Invalid confirmation code.</i>
    .email-code-expired = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The code has expired. Request a new one.</i>
    .email-confirmed = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Email confirmed and linked to your account.</i>

ntf-plan =
    .not-file = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Send the plans as a JSON file.</i>
    .import-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Import failed.</i>
    .import-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Imported successfully.</i>
    .export-plans-not-selected = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Select at least one plan to export.</i>
    .export-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Export failed.</i>
    .export-success = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Selected plans exported.</i>
    .trial-single-duration = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>A trial plan can only have one duration.</i>
    .duration-already-exists = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>This duration already exists.</i>
    .name-already-exists = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>A plan with this name already exists.</i>
    .user-already-allowed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>This user ID has already been added.</i>

    .updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Plan updated successfully.</i>
    .created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Plan created successfully.</i>
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Plan deleted successfully.</i>

ntf-gateway =
    .not-configured = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Payment gateway is not configured.</i>
    .not-configurable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The payment gateway has no settings.</i>
    .test-payment-created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i><a href="{ $url }">Test payment</a> created successfully.</i>
    .test-payment-error = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Error creating the test payment.</i>
    .test-payment-confirmed = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Test payment processed successfully.</i>
    .field-reset = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Field value cleared.</i>
    .field-reset-deactivated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Field value cleared. The gateway was disabled: required settings are missing.</i>

ntf-subscription =
    .plans-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No plans are currently available.</i>
    .gateways-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No payment systems are currently available.</i>
    .renew-plan-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The current plan is outdated and cannot be renewed.</i> Press the <b>"Change"</b> button.
    .payment-creation-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Error creating the payment. Try again later.</i>

ntf-broadcast =
    .text-too-long = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Maximum number of characters exceeded ({ $max_limit }).
    .list-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The broadcast list is empty.</i>
    .plans-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No plans available.</i>
    .audience-unavailable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No users for the selected audience.</i>
    .content-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Content is empty.</i>
    .content-saved = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Content saved successfully.</i>

    .not-cancelable = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>This broadcast cannot be canceled.</i>
    .canceled = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Broadcast canceled successfully.</i>
    .deleting = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Deleting sent messages.</i>
    .already-deleted = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The broadcast has already been deleted or is being deleted.</i>

    .deleted-success =
        ℹ️ Broadcast deletion result <code>{ $task_id }</code>.

        <blockquote>
        • <b>Total messages</b>: { $total_count }
        • <b>Deleted</b>: { $deleted_count }
        • <b>Failed to delete</b>: { $failed_count }
        </blockquote>

ntf-importer =
    .not-file = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Send the database as a file.</i>
    .db-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Error exporting users from the database.</i>
    .users-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The user list in the database is empty.</i>

    .started = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Import started. Please wait for it to finish...</i>
    .already-running = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Import is already running. Please wait.</i>

ntf-sync =
    .from-panel-started = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Panel → bot synchronization started. Please wait for it to finish...</i>
    .from-bot-started = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Bot → panel synchronization started. Please wait for it to finish...</i>
    .users-not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No users found for synchronization.</i>
    .already-running = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>Synchronization is already running. Please wait.</i>

ntf-menu-editor =
    .button-saved = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Button saved successfully.</i>
    .invalid-payload = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Invalid URL format.</i>

ntf-devices =
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Device deleted.</i>
    .all-deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>All devices deleted.</i>
    .reissued = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Subscription reissued successfully.</i>

ntf-backup =
    .assets-started = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> <i>Creating assets backup...</i>
    .db-started = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> <i>Creating database backup...</i>
    .error = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Error creating backup</i>

ntf-blacklist =
    .list-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The blocked list is empty.</i>
    .no-ids-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No IDs found at the link.</i>
    .source-removed = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>List deleted.</i>
    .blocked-ids-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The blocked ID list is empty.</i>
    .blocked-ids-cleared = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Cleared { $count } IDs.</i>
    
    .block-result =
    ℹ️ Blocking result.

    <blockquote>
    • <b>Total IDs</b>: { $total }
    • <b>Users blocked</b>: { $blocked_users }
    • <b>IDs blocked</b>: { $blocked_ids }
    • <b>Already blocked</b>: { $already_blocked }
    </blockquote>

ntf-invite =
    .referral-reset = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Referral link updated.</i>

ntf-promocode =
    .not-found = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Promocode not found or invalid.</i>
    .not-available = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Promocode is unavailable.</i>
    .expired = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The promocode has expired.</i>
    .already-activated = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>You have already activated this promocode.</i>
    .activated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Promocode activated successfully!</i>
    .activation-failed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Failed to activate the promocode. Try again later.</i>
    .code-exists = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>A promocode with this code already exists.</i>
    .created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Promocode created.</i>
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Promocode deleted.</i>
    .fields-required = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>Fill in the reward value.</i>
    .invalid-code = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>The code may contain only Latin letters, digits, hyphens and underscores.</i>
    .plans-empty = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> <i>No plans available.</i>
    .updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Promocode updated.</i>

ntf-ad-link =
    .created = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Ad link created.</i>
    .updated = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Ad link updated.</i>
    .deleted = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> <i>Ad link deleted.</i>

sc-open = { "{" }
sc-close = { "}" }

hdr-email-html =
    <!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>KAGO VPN</title>
    <style>
    @media(max-width:600px){ sc-open }.wrap{ sc-open }padding:16px 8px!important{ sc-close }.card{ sc-open }border-radius:12px!important;border-left:none!important;border-right:none!important;width:100%!important{ sc-close }.hd{ sc-open }padding:28px 20px 24px!important;border-radius:12px 12px 0 0!important{ sc-close }.hd h1{ sc-open }font-size:22px!important{ sc-close }.body,.btns,.foot{ sc-open }padding-left:20px!important;padding-right:20px!important{ sc-close }.btn{ sc-open }padding:14px!important;font-size:14px!important{ sc-close }{ sc-close }
    </style>
    </head><body style="margin:0;padding:0;background:#EEF3FB;font-family:Arial,sans-serif;">

ftr-email-html =
    <tr><td class="foot" align="center" style="background:#F8FAFF;border-top:1px solid #EEF2FF;padding:20px 32px;border-radius:0 0 16px 16px;">
      <p style="margin:0 0 10px;font-size:12px;"><a href="https://usekago.net/help" style="color:#94A3B8;text-decoration:none;margin:0 8px;">Support</a><a href="https://usekago.net/faq" style="color:#94A3B8;text-decoration:none;margin:0 8px;">FAQ</a><a href="https://usekago.net/terms" style="color:#94A3B8;text-decoration:none;margin:0 8px;">Terms</a></p>
      <p style="margin:0;font-size:11px;color:#CBD5E1;line-height:1.7;">© 2026 KAGO VPN · This email was sent automatically. Please do not reply.</p>
    </td></tr>
    </table></td></tr></table></body></html>

email-success-purchase =
    .title = { $purchase_type ->
        [RENEW] Subscription renewed successfully
        [CHANGE] Plan changed successfully
       *[NEW] Purchase completed successfully
        }
    .message =
        { $purchase_type ->
            [RENEW] Your subscription has been renewed.
            [CHANGE] Your plan has been changed.
           *[NEW] Your order has been placed.
        }
        Connection link: { $subscription_url }
        Go to the Telegram bot to manage your subscription: { $bot_url }
        Thank you for choosing us!

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">{ $purchase_type ->
            [RENEW] Your KAGO VPN subscription has been renewed. You can keep using the service.
            [CHANGE] Your KAGO VPN plan has been updated. Reconnect to apply the changes.
           *[NEW] Your KAGO VPN subscription is active. Connect in 2 steps and start using it.
        }</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#16A34A;">&#9679; { $purchase_type ->
            [RENEW] Subscription renewed
            [CHANGE] Plan changed
           *[NEW] Subscription active
        }</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">{ $purchase_type ->
            [RENEW] Welcome back,<br><span style="color:#3B6FD4;">subscription renewed!</span>
            [CHANGE] Plan updated,<br><span style="color:#3B6FD4;">all set!</span>
           *[NEW] Welcome,<br><span style="color:#3B6FD4;">you're protected!</span>
        }</h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">{ $purchase_type ->
            [RENEW] Your subscription has been renewed. You can keep using the service.
            [CHANGE] Your plan has been changed. Reconnect to apply the changes.
           *[NEW] Your subscription has been set up. Follow two steps to get started.
        }</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;">
        <p style="margin:0 0 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94A3B8;">What to do</p>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#3B6FD4;border-radius:50%;text-align:center;line-height:30px;font-size:13px;font-weight:800;color:#fff;">1</div></td><td style="padding-left:12px;"><b style="font-size:14px;color:#1e2a4a;">Connect the VPN</b><br><span style="font-size:13px;color:#64748B;">Press the button below — the configuration will load automatically</span></td></tr></table>
        <div style="width:1px;height:10px;background:#E2E8F0;margin:6px 0 6px 14px;"></div>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#F1F5F9;border:1.5px solid #E2E8F0;border-radius:50%;text-align:center;line-height:27px;font-size:13px;font-weight:800;color:#94A3B8;">2</div></td><td style="padding-left:12px;"><b style="font-size:14px;color:#1e2a4a;">Open Telegram</b><br><span style="font-size:13px;color:#64748B;">After connecting, go to the bot to manage your subscription</span></td></tr></table>
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $subscription_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;margin-bottom:8px;">&#9889; Connect VPN</a>
          <a href="{ $bot_url }" class="btn" style="display:block;padding:13px;background:#F8FAFF;border:1.5px solid #BFDBFE;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:600;color:#3B6FD4;">&#9992;&#65039; Open Telegram</a>
        </td></tr>
        <tr><td style="padding:0 32px;"><div style="height:1px;background:#EEF2FF;"></div></td></tr>
        <tr><td class="stats" style="padding:20px 32px;"><table class="stat" width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #E2E8F0;border-radius:12px;overflow:hidden;"><tr>
          <td align="center" style="background:#F8FAFF;padding:16px 8px;width:33%;"><b style="font-size:14px;color:#1e2a4a;display:block;">{ $expire_date }</b><span style="font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#94A3B8;">Expires</span></td>
          <td align="center" style="background:#F8FAFF;padding:16px 8px;width:34%;border-left:1px solid #E2E8F0;border-right:1px solid #E2E8F0;"><b style="font-size:14px;color:#1e2a4a;display:block;">{ $devices }</b><span style="font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#94A3B8;">Limit</span></td>
          <td align="center" style="background:#F8FAFF;padding:16px 8px;width:33%;"><b style="font-size:14px;color:#1e2a4a;display:block;">{ $plan_name }</b><span style="font-size:10px;text-transform:uppercase;letter-spacing:.07em;color:#94A3B8;">Plan</span></td>
        </tr></table></td></tr>
        { ftr-email-html }

email-failed-purchase =
    .title = Payment failed
    .message =
        Unfortunately, your payment could not be processed.

        Try again or contact support.
        Go to the bot: { $bot_url }

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">Your payment failed — try again or contact support and we'll help you sort it out.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#FFF5F5;border-bottom:1px solid #FED7D7;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#FFF5F5;border:1px solid #FED7D7;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#C53030;">&#9888; Payment failed</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">Something went wrong</h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">Unfortunately, your payment could not be processed. Try again — it only takes a few seconds.</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;">
        <p style="margin:0 0 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94A3B8;">What to do next</p>
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#3B6FD4;border-radius:50%;text-align:center;line-height:30px;font-size:13px;font-weight:800;color:#fff;">1</div></td><td style="padding-left:12px;padding-bottom:12px;"><b style="font-size:14px;color:#1e2a4a;">Go to the bot</b><br><span style="font-size:13px;color:#64748B;">Open Telegram and try to pay again</span></td></tr>
        <tr><td width="30" valign="top"><div style="width:30px;height:30px;background:#F1F5F9;border:1.5px solid #E2E8F0;border-radius:50%;text-align:center;line-height:27px;font-size:13px;font-weight:800;color:#94A3B8;">2</div></td><td style="padding-left:12px;"><b style="font-size:14px;color:#1e2a4a;">Contact support</b><br><span style="font-size:13px;color:#64748B;">If the problem persists — we'll help you sort it out</span></td></tr>
        </table>
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $bot_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;">&#9992;&#65039; Go to the bot</a>
        </td></tr>
        { ftr-email-html }

email-custom-message =
    .title = Message from KAGO VPN
    .message =
        { $body }

        Open the Telegram bot: { $bot_url }

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">You have a new message from KAGO VPN — open the email to see the details.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#3B6FD4;">&#9993; Message</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">We have an<br><span style="color:#3B6FD4;">important message</span> for you</h1>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;font-size:15px;color:#1e2a4a;line-height:1.6;">
          { $body }
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $bot_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;">&#9992;&#65039; Open Telegram</a>
        </td></tr>
        { ftr-email-html }

email-notification =
    .title = Notification from KAGO VPN
    .message =
        { $body }

        Connect the Telegram bot to manage your subscription: { $bot_url }

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">You have a new notification about your KAGO VPN subscription — check the details now.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#3B6FD4;">&#128276; Notification</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">New notification<br><span style="color:#3B6FD4;">from KAGO VPN</span></h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">Connect the Telegram bot to get notifications instantly and manage your subscription in a few clicks.</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;font-size:15px;color:#1e2a4a;line-height:1.6;">
          { $body }
        </td></tr>
        <tr><td class="btns" style="padding:0 32px 28px;">
          <a href="{ $bot_url }" class="btn" style="display:block;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;">&#9992;&#65039; Connect Telegram</a>
          <a href="https://usekago.net/plans" class="btn" style="display:block;margin-top:10px;padding:15px;background:#fff;border:1px solid #3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#3B6FD4;">&#127760; Visit website</a>
        </td></tr>
        { ftr-email-html }

email-verification =
    .title = Your confirmation code — { $code }
    .message =
        Your confirmation code: { $code }

        It is valid for { $minutes } minutes. If you did not request a code, simply ignore this email.{ $has_link ->
            [yes] { "" }

                Or follow the link to log in without entering the code:
                { $link }
           *[other] { "" }
        }

    .message-html =
        { hdr-email-html }
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">Your KAGO VPN confirmation code: { $code }. It is valid for { $minutes } minutes.</span>
        <span style="display:none; max-height:0; overflow:hidden; mso-hide:all;">&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;</span>
        <table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" class="wrap" style="padding:36px 16px;">
        <table class="card" width="560" style="max-width:560px;width:100%;background:#fff;border:1px solid #DDE6F4;border-radius:16px;">
        <tr><td class="hd" align="center" style="background:#EFF6FF;border-bottom:1px solid #DBEAFE;padding:40px 32px 32px;border-radius:16px 16px 0 0;">
        <p style="margin:0 0 16px;"><span style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:100px;padding:4px 14px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.08em;color:#3B6FD4;">&#128274; Email confirmation</span></p>
        <h1 style="margin:0 0 12px;font-size:26px;font-weight:800;color:#1e2a4a;line-height:1.25;">Your confirmation<br><span style="color:#3B6FD4;">code</span></h1>
        <p style="margin:0;font-size:14px;color:#64748B;line-height:1.6;">Enter this code to confirm your email address.</p>
        </td></tr>
        <tr><td class="body" style="padding:28px 32px;">
        <div style="background:#F8FAFF;border:1px solid #DBEAFE;border-radius:12px;padding:24px;text-align:center;">
          <p style="margin:0 0 10px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.1em;color:#94A3B8;">Confirmation code</p>
          <div style="font-size:38px;font-weight:800;letter-spacing:.32em;color:#1e2a4a;font-family:'Courier New',Courier,monospace;">{ $code }</div>
        </div>
        <p style="margin:18px 0 0;font-size:13px;color:#64748B;line-height:1.6;text-align:center;">&#9201; The code is valid for <b style="color:#1e2a4a;">{ $minutes } minutes</b>. Do not share it with anyone.</p>
        { $has_link ->
            [yes] <a href="{ $link }" class="btn" style="display:block;margin-top:20px;padding:15px;background:#3B6FD4;border-radius:10px;text-align:center;text-decoration:none;font-size:15px;font-weight:700;color:#fff;">&#128273; Log in with one tap</a>
           *[other] { "" }
        }
        </td></tr>
        <tr><td style="padding:0 32px;"><div style="height:1px;background:#EEF2FF;"></div></td></tr>
        <tr><td style="padding:20px 32px 8px;"><p style="margin:0;font-size:12px;color:#94A3B8;line-height:1.6;">If you did not request this code, simply ignore this email — nothing will happen to your account.</p></td></tr>
        { ftr-email-html }
