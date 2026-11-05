event-error =
    .general =
    #ErrorEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: An error occurred!</b>

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

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Event: Possible Remnawave incompatibility!</b>

    <blockquote>
    Panel version <b>{ $panel_version }</b> is higher than the tested version <b>{ $max_version }</b>. Some bot features may not work correctly.
    </blockquote>

    { frg-build-info }
    
    .remnawave =
    #RemnawaveErrorEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Remnawave connection error!</b>

    <blockquote>
    The bot cannot work properly without an active connection!
    </blockquote>

    { frg-build-info }

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

    .webhook =
    #ErrorEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Webhook error detected!</b>

    { hdr-error }
    <blockquote>
    { $error }
    </blockquote>

    .channel-check =
    #ChannelCheckErrorEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Event: Channel/group subscription check error!</b>

    { hdr-user }
    { frg-user-info }

    <blockquote>
    • <b>Reason</b>: <code>{ $reason }</code>
    </blockquote>
    
    Make sure the bot is an administrator of the channel/group with permission to view members.

    .notification =
    #NotificationErrorEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Event: System notification delivery error!</b>

    <blockquote>
    • <b>Route</b>: { NUMBER($chat_id, useGrouping: 0) }{ $thread_id ->
        [0] { space }
        *[HAS] :{ NUMBER($thread_id, useGrouping: 0) }
    }
    • <b>Reason</b>: <code>{ $reason }</code>
    </blockquote>

    Check the notification route and make sure the bot is a member of the group with permission to send messages.


event-bot =
    .startup =
    #BotStartupEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Bot started!</b>

    { frg-build-info }

    <b><tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Availability</b>:
    <blockquote>
    • <b>Mode</b>: { access-mode }
    • <b>Payments</b>: { $payments_allowed ->
    [0] disabled
    *[1] enabled
    }
    • <b>Registration</b>: { $registration_allowed ->
    [0] disabled
    *[1] enabled
    }
    </blockquote>

    .inline-mode-disabled =
    #BotInlineModeDisabledEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Event: Inline mode is disabled in BotFather!</b>

    <blockquote>
    The bot is not configured for inline mode. Some bot features may not work correctly.

    Enable Inline Mode in BotFather: <b>@BotFather → /mybots → Bot Settings → Inline Mode → Enable</b>
    </blockquote>

    .shutdown =
    #BotShutdownEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Bot stopped!</b>

    { frg-build-info }

    <blockquote>
    • <b>Uptime</b>: { $uptime }
    </blockquote>

    .update =
    #BotUpdateEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Remnashop update detected!</b>

    <b><tg-emoji emoji-id="6050643982646513651">📑</tg-emoji> Versions</b>:
    <blockquote>
    • <b>Current</b>: { $local_version }
    • <b>Latest</b>: { $remote_version }
    </blockquote>


event-user =
    .registered =
    #UserRegisteredEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: New user!</b>

    { hdr-user }
    { frg-user-info }

    { $referrer_user_id ->
    [0] { empty }
    *[HAS]
    <b><tg-emoji emoji-id="5891207662678317861">🤝</tg-emoji> Referrer</b>:
    <blockquote>
    { $referrer_telegram_id ->
        [0] • <b>Email</b>: <code>{ $referrer_email }</code>
        *[HAS] • <b>ID</b>: <code>{ NUMBER($referrer_telegram_id, useGrouping: 0) }</code>
    }
    • <b>Name</b>: { $referrer_name } { $referrer_username ->
        [0] { empty }
        *[HAS] (<a href="tg://user?id={ $referrer_telegram_id }">@{ $referrer_username }</a>)
    }
    </blockquote>
    }

    { $ad_link_id ->
    [0] { empty }
    *[HAS]
    <b><tg-emoji emoji-id="6032949275732742941">🎯</tg-emoji> Ad link</b>:
    <blockquote>
    • <b>Name</b>: { $ad_link_name }
    • <b>Code</b>: <code>{ $ad_link_code }</code>
    </blockquote>
    }

    .first-connected =
    #UserFirstConnectionEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: User's first connection!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-subscription }
    { frg-subscription-details }

    .device-added =
    #UserDeviceAddedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: User added a new device!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }

    .device-deleted =
    #UserDeviceDeletedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: User deleted a device!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-hwid }
    { frg-user-hwid }


event-blacklist =
    .registration-attempt =
    #BlacklistRegistrationAttemptEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Registration attempt from blacklist!</b>

    { hdr-user }
    { frg-user-info }


event-subscription =
    .trial =
    #SubscriptionTrialEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Trial subscription received!</b>

    { hdr-user }
    { frg-user-info }
    
    { hdr-plan }
    { frg-plan-snapshot }
    
    .new =
    #SubscriptionNewEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Subscription purchased!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

    .renew =
    #SubscriptionRenewEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Subscription renewed!</b>
    
    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot }

    .change =
    #SubscriptionChangeEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Subscription changed!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    { hdr-plan }
    { frg-plan-snapshot-comparison }

    .expiring =
    { $is_trial ->
    [0]
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Attention! Your subscription will expire in { $duration }.</b>
    
    Renew it in advance so you don't lose access to the service! 
    *[1]
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Attention! Your free trial will end in { $duration }.</b>

    Get a subscription so you don't lose access to the service! 
    }

    .expired =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Attention! Access suspended — the VPN is not working.</b>

    { $is_trial ->
    [0] Your subscription has expired, renew it to keep using the VPN!
    *[1] Your free trial has ended. Get a subscription to keep using the service!
    }

    .expired-ago =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Attention! Access suspended — the VPN is not working.</b>

    { $is_trial ->
    [0] Your subscription expired { $duration } ago, renew it to keep using the service!
    *[1] Your free trial ended { $duration } ago. Get a subscription to keep using the service!
    }

    .limited =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Attention! Access suspended — the VPN is not working.</b>

    Your traffic has been used up. { $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Renew your subscription to reset your traffic and keep using the service!
        *[RESET] Your traffic will be restored in { $reset_time }. You can also renew your subscription to reset it.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Get a subscription to keep using the service!
        *[RESET] Your traffic will be restored in { $reset_time }. You can also get a subscription to use the service without limits.
        }
    }

    .not-connected =
    <b>🔌 Having trouble connecting?</b>

    If you have trouble setting up the VPN, we're ready to help! Contact support and we'll sort it out together.

    .revoked =
    #SubscriptionRevokedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: User reissued their subscription!</b>

    { hdr-user }
    { frg-user-info }

    { hdr-subscription }
    { frg-subscription-details }


event-node =
    .connection-lost =
    #NodeConnectionLostEvent
    
    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Node connection lost!</b>

    { hdr-node }
    { frg-node-info }

    .connection-restored =
    #NodeConnectionRestoredEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Node connection restored!</b>

    { hdr-node }
    { frg-node-info }

    .traffic-reached =
    #NodeTrafficReachedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Node reached its traffic limit threshold!</b>

    { hdr-node }
    { frg-node-info }

    .billing-payment =
    #NodeBillingPaymentEvent

    <b><tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Event: { $reminder ->
        [in-7-days] Node payment due in 7 days
        [in-48hrs] Node payment due in 48 hours
        [in-24hrs] Node payment due in 24 hours
        [due-today] Node payment due today!
        [overdue-24hrs] Node payment overdue by 24 hours!
        [overdue-48hrs] Node payment overdue by 48 hours!
        [overdue-7-days] Node payment overdue by 7 days!
        *[OTHER] Node payment reminder
    }</b>

    { hdr-node }
    <blockquote>
    • <b>Name</b>: { $node_name }
    • <b>Provider</b>: { $provider_name }
    • <b>Payment date</b>: { $next_billing_at }
    </blockquote>


event-torrent-blocker =
    .user-blocked =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Server access is temporarily restricted.</b>

    BitTorrent traffic was detected on node <b>{ $node_name }</b>.
    The restriction will remain in effect for another <b>{ $block_duration }</b>.

    If you need help setting up your connection, contact support.

    .report =
    #TorrentBlockedEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Event: BitTorrent traffic detected!</b>

    { hdr-user }
    { frg-user-info }

    <blockquote>
    • <b>Node</b>: { $node_name }
    • <b>IP</b>: <code>{ $blocked_ip }</code>
    • <b>Block duration</b>: { $block_duration }
    • <b>Unblock time</b>: { $will_unblock_at }
    • <b>Protocol</b>: <code>{ $protocol }</code>
    • <b>Source</b>: <code>{ $source }</code>
    • <b>Destination</b>: <code>{ $destination }</code>
    </blockquote>


event-referral =
    .attached =
    <b><tg-emoji emoji-id="6041731551845159060">🎉</tg-emoji> You invited a friend!</b>
    
    <blockquote>
    User <b>{ $name }</b> joined via your invitation link! To receive the reward, make sure they purchase a subscription.
    </blockquote>

    .reward =
    <b><tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> You received a reward!</b>
    
    <blockquote>
    User <b>{ $name }</b> made a payment. You received { $reward_type ->
    [POINTS] <b>{ $value } { $value -> 
        [one] point
        *[more] points
        }</b>

    <i>To use your points, go to the "Invite" section in the bot to learn about available rewards and how to use them.</i>
    [EXTRA_DAYS] <b>{ $value } extra { $value -> 
        [one] day
        *[more] days
        }</b> added to your subscription!
    *[OTHER] <b>{ $value } { $reward_type }</b>
    }
    </blockquote>

    .reward-failed =
    <b><tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Failed to issue the reward!</b>
    
    <blockquote>
    User <b>{ $name }</b> made a payment, but we couldn't credit your reward because <b>you don't have a purchased subscription</b> to add { $value } { $reward_type ->
    [POINTS] { $value -> 
        [one] point
        *[more] points
        }
    [EXTRA_DAYS] extra { $value -> 
        [one] day
        *[more] days
        }
    *[OTHER] { $reward_type }
    }.
    
    <i>Buy a subscription to get bonuses for invited friends!</i>
    </blockquote>

event-birthday =
    .greeting =
    <b>🎂 Happy birthday, { $name }!</b>

    <blockquote>
    The KAGO team wishes you a wonderful day! May this year be bright, calm and full of good moments.
    </blockquote>

    { $gift ->
    [DAYS]
    🎁 As a gift, we added <b>{ $days } { $days ->
        [one] day
        *[other] days
        }</b> to your subscription.
    [UNLIMITED]
    🎁 Your subscription is already permanent, so we simply wish you a great day!
    *[NONE]
    🎁 Get a subscription, and on your next birthday we will gift you extra days.
    }

event-promocode =
    .activated =
    #PromocodeActivatedEvent

    <b><tg-emoji emoji-id="5884428842780594914">🔅</tg-emoji> Event: Promocode activated!</b>

    { hdr-user }
    { frg-user-info }

    <b><tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Promocode</b>:
    <blockquote>
    • <b>Code</b>: <code>{ $promocode_code }</code>
    • <b>Type</b>: { promocode-type }
    • <b>Reward</b>: { frg-promocode-reward }
    </blockquote>

event-payment =
    .refunded =
    #PaymentRefundedEvent

    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Event: Payment refunded!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    Manual review required — the user's subscription may have remained active.

    .referral-failed =
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Failed to credit the referral reward</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    The purchase completed successfully, but an error occurred while crediting the referral reward. Manual review required.

    .purchase-failed =
    <b><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Event: Payment processing error!</b>

    { hdr-payment }
    { frg-payment-info }

    { hdr-user }
    { frg-user-info }

    Payment received, but the subscription could not be issued. The transaction is marked as FAILED. Manual review required.

event-remnashop-welcome =
    <b><tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Remnashop v{ $version }</b>

    The project is created and maintained by just one <strike>developer</strike> electrician. Since the bot is completely FREE and open source, it exists only thanks to your support.

    <tg-emoji emoji-id="6034923938486684992">⭐</tg-emoji> <i>Give us a star on <a href="{ $repository }">GitHub</a> and join our <a href="https://t.me/@remna_shop">community</a>.</i>

    <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> <i>There is also a <a href="https://boosty.to/snoups/purchase/3778398?ssource=DIRECT&amp;share=subscription_link">private chat</a> for donors.</i>