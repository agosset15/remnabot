# Menu
msg-main-menu =
    { hdr-user-profile }
    { frg-user }
    { $has_pending_email ->
        [0] { empty }
        *[other] <b>Pending confirmation:</b> <code>{ $pending_email }</code>
    }

    { hdr-subscription }
    { $status ->
    [ACTIVE]
    { frg-subscription }
    [EXPIRED]
    <blockquote>
    • Subscription has expired.
    
    <i>{ $is_trial ->
    [0] Your subscription has expired. Renew it to keep using the service!
    *[1] Your free trial has ended. Get a subscription to keep using the service!
    }</i>
    </blockquote>
    [LIMITED]
    <blockquote>
    • Your traffic has been used up.

    <i>{ $is_trial ->
    [0] { $traffic_strategy ->
        [NO_RESET] Renew your subscription to reset your traffic and keep using the service!
        *[RESET] Your traffic will be restored in { $reset_time }. You can also renew your subscription to reset it.
        }
    *[1] { $traffic_strategy ->
        [NO_RESET] Get a subscription to keep using the service!
        *[RESET] Your traffic will be restored in { $reset_time }. You can also get a subscription to use the service without limits.
        }
    }</i>
    </blockquote>
    [DISABLED]
    <blockquote>
    • Your subscription is disabled.

    <i>Contact support to find out why!</i>
    </blockquote>
    *[NONE]
    <blockquote>
    • You don't have a subscription.

    <i>{ $trial_available ->
    [1] <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> A free trial is available to you — press the button below to get it.
    *[0] ↘️ To buy access, go to the "Subscription" menu.
    }</i>
    </blockquote>
    }

msg-menu-devices =
    <b><tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Device management</b>

    Connected: <b>{ $current_count } / { $max_count -> 
    [0] { unlimited }
    *[LIMIT] { $max_count }
    }</b>

    { $has_devices ->
    [0] { empty }
    *[HAS] { $device_single_enabled ->
        [0] To unlink a device, contact support.
        *[OTHER] Tap a device to delete it.
        }
    }{ $max_count ->
    [0] { space }
    *[LIMIT] If the device limit isn't enough, change your subscription.
    }

msg-menu-devices-confirm-reissue =
    <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> <b>Subscription reissue</b>

    <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> After the reset, the old link will <b>stop working</b> and all devices will have to be reconnected.

    You will need to:
    • Remove the old subscription from the app
    • Add the new link from the "{ btn-menu.connect }" section

    Are you sure you want to reset the link?

msg-menu-devices-confirm-delete =
    <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> <b>Confirm device deletion</b>

    <b>{ $device_model }</b>
    <blockquote>
    • <b>Platform</b>: { $platform_icon } { $platform }
    • <b>Added</b>: { $created_at }
    </blockquote>

msg-menu-devices-confirm-delete-all =
    <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> <b>Confirm deletion of all devices</b>

msg-menu-invite =
    <b><tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Invite friends</b>
    
    Share your unique link and get a reward in the form of { $reward_type ->
        [POINTS] <b>points that can be exchanged for a subscription or real money</b>
        [EXTRA_DAYS] <b>free days added to your subscription</b>
        *[OTHER] { $reward_type }
    }!

    <b><tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Statistics</b>:
    <blockquote>
    <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Total invited: { $referrals }
    <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Payments via your link: { $payments }
    { $reward_type -> 
    [POINTS] <tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Your points: { $points }
    *[EXTRA_DAYS] { empty }
    }
    </blockquote>

msg-menu-invite-about =
    <b><tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> About the reward</b>

    <b><tg-emoji emoji-id="5890925363067886150">✨</tg-emoji> How to get the reward</b>:
    <blockquote>
    { $accrual_strategy ->
    [ON_FIRST_PAYMENT] The reward is credited for the invited user's first subscription purchase.
    [ON_EACH_PAYMENT] The reward is credited for every subscription purchase or renewal by the invited user.
    *[OTHER] { $accrual_strategy }
    }
    </blockquote>

    <b><tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> What you get</b>:
    <blockquote>
    { $max_level -> 
    [1] For invited friends: { $reward_level_1 }
    *[MORE]
    { $identical_reward ->
    [0]
    <tg-emoji emoji-id="5794164805065514131">1️⃣</tg-emoji> For your friends: { $reward_level_1 }
    <tg-emoji emoji-id="5794085322400733645">2️⃣</tg-emoji> For those invited by your friends: { $reward_level_2 }
    *[1]
    For your friends and those invited by your friends: { $reward_level_1 }
    }
    }
    
    { $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [POINTS] { space }
        [EXTRA_DAYS] <i>(All extra days are added to your current subscription)</i>
        *[OTHER] { $reward_type }
    }
    [PERCENT] { $reward_type ->
        [POINTS] <i>(Percentage of points from the price of their purchased subscription)</i>
        [EXTRA_DAYS] <i>(Percentage of extra days from their purchased subscription)</i>
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }
    </blockquote>

msg-invite-reward = { $value }{ $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [POINTS] { space }{ $value -> 
            [one] point
            *[more] points
            }
        [EXTRA_DAYS] { space }extra { $value -> 
            [one] day
            *[more] days
            }
        *[OTHER] { $reward_type }
    }
    [PERCENT] % { $reward_type ->
        [POINTS] points
        [EXTRA_DAYS] extra days
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }


# Dashboard
msg-dashboard-main = <b><tg-emoji emoji-id="5771449289972650710">🛠</tg-emoji> Dashboard</b>
msg-users-main = <b><tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Users</b>
msg-broadcast-main = <b><tg-emoji emoji-id="6021418126061605425">📢</tg-emoji> Broadcast</b>
msg-statistics-main = <b><tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Statistics</b>
    
msg-statistics-users =
    <b><tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> User statistics</b>

    <blockquote>
    • <b>Total</b>: { $total_users }
    • <b>New today</b>: { $new_users_daily }
    • <b>New this week</b>: { $new_users_weekly }
    • <b>New this month</b>: { $new_users_monthly }

    • <b>With subscription</b>: { $users_with_subscription }
    • <b>Without subscription</b>: { $users_without_subscription }
    • <b>With trial</b>: { $users_with_trial }
    </blockquote>

    <blockquote>
    • <b>Blocked</b>: { $blocked_users }
    • <b>Blocked the bot</b>: { $bot_blocked_users }

    • <b>Conversion: users → purchase</b>: { $user_conversion }%
    • <b>Conversion: trials → subscription</b>: { $trial_conversion }%
    </blockquote>

msg-statistics-subscriptions =
    { $plan_name ->
    [0] <b><tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Subscription statistics</b>
    *[HAS] <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Plan statistics "{ $plan_name }"</b>
    }

    <blockquote>
    • <b>Total</b>: { $total }
    • <b>Active</b>: { $total_active }
    • <b>Disabled</b>: { $total_disabled }
    • <b>Limited</b>: { $total_limited }
    • <b>Expired</b>: { $total_expired }
    • <b>Expiring (7 days)</b>: { $expiring_soon }
    { $plan_name ->
    [0] • <b>Trial</b>: { $active_trial }
    *[HAS] • <b>Popular duration</b>: { $popular_duration }
    }
    </blockquote>

    { $plan_name ->
    [0] <blockquote>
    • <b>Unlimited</b>: { $total_unlimited }
    • <b>With traffic limit</b>: { $total_traffic }  
    • <b>With device limit</b>: { $total_devices }
    </blockquote>
    *[HAS] <b>Total income</b>:
    <blockquote>
    { $all_income }
    </blockquote>
    }
    
msg-statistics-subscriptions-plan-income = { $income }{ $currency }
    
msg-statistics-transactions =
    { $gateway_type ->
    [0] <b><tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Overall transaction statistics</b>
    *[HAS] <b><tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> { gateway-type } statistics</b>
    }

    <blockquote>
    • <b>Total transactions</b>: { $total_transactions }
    • <b>Completed transactions</b>: { $completed_transactions }
    • <b>Free transactions</b>: { $free_transactions }
    { $gateway_type ->
    [0] { $popular_gateway ->
        [0] { empty }
        *[HAS] • <b>Popular payment system</b>: { $popular_gateway }
        }
    *[HAS] { empty }
    }
    </blockquote>

    { $gateway_type ->
    [0] { empty }
    *[HAS] <blockquote>
    • <b>Total income</b>: { $total_income }{ $currency }
    • <b>Income today</b>: { $daily_income }{ $currency }
    • <b>Income this week</b>: { $weekly_income }{ $currency }
    • <b>Income this month</b>: { $monthly_income }{ $currency }
    • <b>Income last month</b>: { $last_month_income }{ $currency }
    • <b>Average check</b>: { $average_check }{ $currency }
    • <b>Total discounts</b>: { $total_discounts }{ $currency }
    </blockquote>
    }

msg-statistics-promocodes =
    <b><tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Promocode statistics</b>

    <blockquote>
    • <b>Total promocodes</b>: { $total_promocodes }
    • <b>Active</b>: { $active_promocodes }
    • <b>Total activations</b>: { $total_activations }
    </blockquote>

    <blockquote>
    • <b>Activations today</b>: { $activations_today }
    • <b>Activations this week</b>: { $activations_week }
    • <b>Activations this month</b>: { $activations_month }
    </blockquote>

    <blockquote>
    • <b>Days issued</b>: { $issued_days }
    • <b>Traffic issued (GB)</b>: { $issued_traffic }
    • <b>Devices issued</b>: { $issued_devices }
    • <b>Subscriptions issued</b>: { $issued_subscriptions }
    • <b>Personal discounts issued</b>: { $issued_personal_discounts }
    • <b>One-time discounts issued</b>: { $issued_purchase_discounts }
    </blockquote>

msg-statistics-promocode-detail =
    <b><tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Promocode</b> <code>{ $code }</code>

    <blockquote>
    • <b>Type</b>: { promocode-type }
    • <b>Reward</b>: { $reward }
    • <b>Status</b>: { $is_active ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
        }
    • <b>Reactivation</b>: { $is_reusable ->
        [1] Allowed
        *[0] Forbidden
        }
    </blockquote>

    <blockquote>
    • <b>Created</b>: { $created_at }
    • <b>Valid until</b>: { $expires_at }
    • <b>Activation limit</b>: { $max_activations }
    • <b>Activations remaining</b>: { $remaining }
    </blockquote>

    <blockquote>
    • <b>Total activations</b>: { $total_activations }
    • <b>Today</b>: { $activations_today }
    • <b>This week</b>: { $activations_week }
    • <b>This month</b>: { $activations_month }
    </blockquote>

msg-statistics-referrals =
    <b><tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Referral statistics</b>

    <blockquote>
    • <b>Total referrals</b>: { $total_referrals }
    • <b>Level 1</b>: { $level_1_count }
    • <b>Level 2</b>: { $level_2_count }
    • <b>Unique referrers</b>: { $unique_referrers }
    { $top_referrer_id ->
        [0] { empty }
        *[HAS] • <b>Top referrer</b>: { $top_referrer_telegram_id ->
            [0] <code>{ $top_referrer_email }</code>
            *[HAS] { $top_referrer_username ->
                [0] { NUMBER($top_referrer_telegram_id, useGrouping: 0) }
                *[HAS] <a href="tg://user?id={ $top_referrer_telegram_id }">@{ $top_referrer_username }</a>
            }
        } ({ $top_referrer_referrals_count } invited)
    }
    </blockquote>

    <blockquote>
    • <b>Rewards issued</b>: { $total_rewards_issued }
    • <b>Points issued</b>: { $total_points_issued }
    • <b>Days issued</b>: { $total_days_issued }
    </blockquote>


# Access
msg-access-main =
    <b><tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Access mode</b>
    
    <blockquote>
    • <b>Mode</b>: { access-mode }
    • <b>Payments</b>: { $payments_allowed ->
    [0] disabled
    *[1] enabled
    }.
    • <b>Registration</b>: { $registration_allowed ->
    [0] disabled
    *[1] enabled
    }.
    </blockquote>

msg-access-conditions =
    <b><tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> Access conditions</b>

msg-access-rules =
    <b>✳️ Change rules link</b>

    { $rules_url ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $rules_url }
    </blockquote>
    }

    Enter the link (in the format https://telegram.org/tos).

msg-access-channel =
    <b>❇️ Change channel/group link</b>

    { $channel_url ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $channel_url } { $channel_id -> 
        [0] { empty } 
        *[HAS] (ID: { $channel_id }) 
        }
    </blockquote>
    }
    
    If your group has no @username, send the group ID and the invite link as separate messages.
    
    If you have a public channel/group, enter only the @username.


# Broadcast
msg-broadcast-list = <b><tg-emoji emoji-id="6037475557082403885">📄</tg-emoji> Broadcast list</b>
msg-broadcast-plan-select = <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Select a plan for the broadcast</b>
msg-broadcast-send = <b><tg-emoji emoji-id="6021418126061605425">📢</tg-emoji> Send broadcast ({ audience-type })</b>

    { $audience_count } { $audience_count ->
    [one] user
    *[more] users
    } will receive the broadcast

msg-broadcast-content =
    <b><tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Broadcast content</b>

    Send a message (HTML is supported). You can attach a photo, video or file. Limit: up to 4096 characters without media, up to 1024 characters with media.

msg-broadcast-buttons = <b>✳️ Broadcast buttons</b>

msg-broadcast-view =
    <b><tg-emoji emoji-id="6021418126061605425">📢</tg-emoji> Broadcast</b>

    <blockquote>
    • <b>ID</b>: <code>{ $broadcast_id }</code>
    • <b>Status</b>: { broadcast-status }
    • <b>Audience</b>: { audience-type }
    • <b>Created</b>: { $created_at }
    </blockquote>

    <blockquote>
    • <b>Total messages</b>: { $total_count }
    • <b>Successful</b>: { $success_count }
    • <b>Failed</b>: { $failed_count }
    </blockquote>


# Users
msg-users-recent-registered = <b><tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Recently registered</b>
msg-users-recent-activity = <b><tg-emoji emoji-id="6039614175917903752">📝</tg-emoji> Recently active</b>
msg-user-transactions = <b><tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> User transactions</b>
msg-user-devices = <b><tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> User devices ({ $current_count } / { $max_count })</b>
msg-user-give-access = <b>🔑 Grant access to a plan</b>

msg-users-search =
    <b><tg-emoji emoji-id="6032850693348399258">🔍</tg-emoji> User search</b>

    Enter the user's ID or email, part of the name, or forward any message from them.

msg-users-search-results =
    <b><tg-emoji emoji-id="6032850693348399258">🔍</tg-emoji> User search</b>

    Found <b>{ $count }</b> { $count ->
    [one] user
    *[more] users
    } matching the query

msg-user-main = 
    <b><tg-emoji emoji-id="6039614175917903752">📝</tg-emoji> User information</b>

    { hdr-user-profile }
    { frg-user-details }

    <b><tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Discount</b>:
    <blockquote>
    • <b>Personal</b>: { $personal_discount }%
    • <b>On next purchase</b>: { $purchase_discount }%
    </blockquote>
    
    { hdr-subscription }
    { $status ->
    [ACTIVE]
    { frg-subscription-user-editor }
    [EXPIRED]
    <blockquote>
    • Subscription has expired.
    </blockquote>
    [LIMITED]
    <blockquote>
    • Traffic limit exceeded.
    </blockquote>
    [DISABLED]
    <blockquote>
    • Subscription disabled.
    </blockquote>
    *[NONE]
    <blockquote>
    • No current subscription.
    </blockquote>
    }

msg-user-statistics =
    <b><tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> User statistics</b>

    <blockquote>
    • <b>Registration date</b>: { $registered_at }
    • <b>Last payment</b>: { $last_payment_at ->
        [0] { unknown }
        *[HAS] { $last_payment_at }
    }
    </blockquote>

    { $payment_amounts ->
    [0] { space }
    *[HAS] <blockquote>
    { $payment_amounts }
    </blockquote>
    }

    <blockquote>
    • <b>Invited by</b>: { $referrer_telegram_id ->
        [0] { $referrer_email ->
            [0] { unknown }
            *[HAS] <code>{ $referrer_email }</code>
        }
        *[HAS] { $referrer_username ->
            [0] { NUMBER($referrer_telegram_id, useGrouping: 0) }
            *[HAS] <a href="tg://user?id={ $referrer_telegram_id }">@{ $referrer_username }</a>
        }
    }
    • <b>Invited (lvl 1)</b>: { $referrals_level_1 }
    • <b>Invited (lvl 2)</b>: { $referrals_level_2 }
    • <b>Points received</b>: { $reward_points }
    • <b>Days received</b>: { $reward_days }
    </blockquote>

msg-user-statistics-payment-amount = • <b>Paid ({ $currency })</b>: { $amount }

msg-user-referrals = <b><tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> User referrals</b>

msg-user-sync = 
    <b><tg-emoji emoji-id="5769248574499983619">🌀</tg-emoji> Synchronize user</b>

    <b><tg-emoji emoji-id="5920332557466997677">🛍</tg-emoji> Remnashop</b>: { $bot_version }
    <blockquote>
    { $has_bot_subscription -> 
    [0] No data
    *[HAS]{ $bot_subscription }
    }
    </blockquote>

    <b>🌊 Remnawave</b>: { $remna_version }
    <blockquote>
    { $has_remna_subscription -> 
    [0] No data
    *[HAS] { $remna_subscription }
    }
    </blockquote>

    Select the data source for synchronization.

msg-user-sync-version = { $version ->
    [NEWER] (newer)
    [OLDER] (older)
    *[UNKNOWN] { empty }
    }

msg-user-sync-subscription =
    • <b>ID</b>: <code>{ $id }</code>
    • Status: { $status -> 
    [ACTIVE] Active
    [DISABLED] Disabled
    [LIMITED] Traffic exhausted
    [EXPIRED] Expired
    [DELETED] Deleted
    *[OTHER] { $status }
    }
    • Link: <a href="{ $url }">*********</a>

    • Traffic limit: { $traffic_limit }
    • Device limit: { $device_limit }
    • Remaining: { $expire_time }

    • Internal squads: { $internal_squads ->
    [0] { unknown }
    *[HAS] { $internal_squads }
    }
    • External squad: { $external_squad ->
    [0] { unknown }
    *[HAS] { $external_squad }
    }
    • Traffic reset: { $traffic_limit_strategy -> 
    [NO_RESET] On payment
    [DAY] Every day
    [WEEK] Every week
    [MONTH] Every month
    [MONTH_ROLLING] Every month (by creation date)
    *[OTHER] { $traffic_limit_strategy }
    }
    • Tag: { $tag -> 
    [0] { unknown }
    *[HAS] { $tag }
    }

msg-user-sync-waiting =
    <b><tg-emoji emoji-id="5769248574499983619">🌀</tg-emoji> User synchronization</b>

    Please wait... User data is being synchronized. You will automatically return to the user editor when it finishes.

msg-user-give-subscription =
    <b><tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Give subscription</b>

    Select the plan you want to give to the user.

msg-user-give-subscription-duration =
    <b><tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Select duration</b>

    Select the duration of the subscription to give.

msg-user-discount =
    <b><tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Change discount</b>

    Select the discount type to change.

msg-user-discount-personal =
    <b><tg-emoji emoji-id="6035084557378654059">👤</tg-emoji> Personal discount</b>

    Choose with a button or enter your own value.

msg-user-discount-purchase =
    <b><tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Next purchase discount</b>

    Choose with a button or enter your own value.
    The discount will be applied once and reset after any payment.

msg-user-points =
    <b><tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Change referral points</b>

    <b>Current points: { $current_points }</b>

    Choose with a button or enter your own value to add or subtract.

msg-user-subscription-traffic-limit =
    <b><tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Change traffic limit</b>

    Choose with a button or enter your own value (in GB) to change the traffic limit.

msg-user-subscription-device-limit =
    <b><tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Change device limit</b>

    Choose with a button or enter your own value to change the device limit.

msg-user-subscription-expire-time =
    <b><tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Change expiration</b>

    <b>Expires in: { $expire_time }</b>

    Choose with a button or enter your own value (in days) to add or subtract.

msg-user-subscription-squads =
    <b><tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Change squad list</b>

    { $internal_squads ->
    [0] { empty }
    *[HAS] <b><tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Internal</b>: { $internal_squads }
    }

    { $external_squad ->
    [0] { empty }
    *[HAS] <b><tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> External</b>: { $external_squad }
    }

msg-user-subscription-internal-squads =
    <b><tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Change internal squad list</b>

    Select which internal groups will be assigned to this user.

msg-user-subscription-external-squads =
    <b><tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> Change external squad</b>

    Select which external group will be assigned to this user.

msg-user-subscription-info =
    <b><tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Current subscription information</b>
    
    { hdr-subscription }
    { frg-subscription-details }

    <blockquote>
    • <b>Internal squads</b>: { $internal_squads ->
    [0] { unknown }
    *[HAS] { $internal_squads }
    }
    • <b>External squad</b>: { $external_squad ->
    [0] { unknown }
    *[HAS] { $external_squad }
    }
    • <b>First connection</b>: { $first_connected_at -> 
    [0] { unknown }
    *[HAS] { $first_connected_at }
    }
    • <b>Last connection</b>: { $last_connected_at ->
    [0] { unknown }
    *[HAS] { $last_connected_at } ({ $node_name })
    } 
    </blockquote>

    { hdr-plan }
    { frg-plan-snapshot }

msg-user-transaction-info =
    <b><tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Transaction information</b>

    { hdr-payment }
    <blockquote>
    • <b>ID</b>: <code>{ $payment_id }</code>
    • <b>User</b>: { $user_name } ({ $user_telegram_id ->
        [0] <code>{ $user_email }</code>
        *[HAS] <code>{ NUMBER($user_telegram_id, useGrouping: 0) }</code>
    })
    • <b>Type</b>: { purchase-type }
    • <b>Status</b>: { transaction-status }
    • <b>Payment method</b>: { gateway-type }
    • <b>Amount</b>: { frg-payment-amount }
    • <b>Created</b>: { $created_at }
    </blockquote>

    { $is_test -> 
    [1] <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Test transaction
    *[0]
    { hdr-plan }
    { frg-plan-snapshot }
    }
    
msg-user-role = 
    <b><tg-emoji emoji-id="6030445631921721471">👮‍♂️</tg-emoji> Change role</b>
    
    Select a new role for the user.

msg-users-blacklist =
    <b><tg-emoji emoji-id="5938215362473496448">🚫</tg-emoji> Blacklist</b>

msg-users-blacklist-list =
    <b><tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Blocked users</b>

    Blocked: <b>{ $count_blocked }</b> / <b>{ $count_users }</b> ({ $percent }%).

msg-users-blacklist-block =
    <b><tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Block by ID</b>

    Supported formats
    <blockquote>
    • <b>Text</b>: enter one ID or a list of IDs
    • <b>Link</b>: send a URL with a list of IDs
    • <b>File</b>: attach a .txt file with a list of IDs
    </blockquote>

    For lists: each ID must be on a new line.

    The block applies even if the user has never used the bot.

msg-users-blacklist-sources =
    <b><tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Auto-updated blacklists</b>

    Tap a list to delete it.
    Synchronization runs automatically every 6 hours.

    To add a new list, send a direct link to a text file with Telegram IDs.

msg-user-message =
    <b><tg-emoji emoji-id="6039391666547201160">📩</tg-emoji> Send a message to the user</b>

    Send any message: text, an image, or both together (HTML is supported).
    

# RemnaWave
msg-remnawave-main =
    <b>🌊 RemnaWave v{ $version }</b>
    
    <b><tg-emoji emoji-id="5942734685976138521">🖥️</tg-emoji> System</b>:
    <blockquote>
    • <b>CPU</b>: { $cpu_cores } { $cpu_cores ->
    [one] core
    *[more] cores
    }
    • <b>RAM</b>: { $ram_used } / { $ram_total } ({ $ram_used_percent }%)
    • <b>Uptime</b>: { $uptime }
    </blockquote>

msg-remnawave-users =
    <b><tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Users</b>

    <b><tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Statistics</b>:
    <blockquote>
    • <b>Total</b>: { $users_total }
    • <b>Active</b>: { $users_active }
    • <b>Disabled</b>: { $users_disabled }
    • <b>Limited</b>: { $users_limited }
    • <b>Expired</b>: { $users_expired }
    </blockquote>

    <b>🟢 Online</b>:
    <blockquote>
    • <b>Today</b>: { $online_last_day }
    • <b>This week</b>: { $online_last_week }
    • <b>Never connected</b>: { $online_never }
    • <b>Online now</b>: { $online_now }
    </blockquote>

msg-remnawave-host-details =
    <b>{ $remark } ({ $is_disabled ->
    [1] disabled
    *[0] enabled
    })</b>:
    <blockquote>
    • <b>Address</b>: <code>{ $address }:{ $port }</code>
    { $inbound_uuid ->
    [0] { empty }
    *[HAS] • <b>Inbound</b>: <code>{ $inbound_uuid }</code>
    }
    </blockquote>

msg-remnawave-node-details =
    <b>{ $country } { $name } ({ $is_connected ->
    [1] connected
    *[0] disconnected
    })</b>:
    <blockquote>
    • <b>Address</b>: <code>{ $address }{ $port -> 
    [0] { empty }
    *[HAS]:{ $port }
    }</code>
    • <b>Uptime (xray)</b>: { $xray_uptime }
    • <b>Users online</b>: { $users_online }
    • <b>Traffic</b>: { $traffic_used } / { $traffic_limit }
    </blockquote>

msg-remnawave-inbound-details =
    <b><tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> { $tag }</b>
    <blockquote>
    • <b>ID</b>: <code>{ $inbound_id }</code>
    • <b>Protocol</b>: { $type } { $network -> 
    [0] { space }
    *[HAS] ({ $network })
    }
    { $port ->
    [0] { empty }
    *[HAS] • <b>Port</b>: { $port }
    }
    { $security ->
    [0] { empty }
    *[HAS] • <b>Security</b>: { $security } 
    }
    </blockquote>

msg-remnawave-hosts =
    <b><tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Hosts</b>

    { $is_empty ->
    [1] <i>No hosts</i>
    *[0] { $host }
    }

msg-remnawave-nodes =
    <b><tg-emoji emoji-id="5942734685976138521">🖥️</tg-emoji> Nodes</b>

    { $is_empty ->
    [1] <i>No nodes</i>
    *[0] { $node }
    }

msg-remnawave-inbounds =
    <b>🔌 Inbounds</b>

    { $is_empty ->
    [1] <i>No inbounds</i>
    *[0] { $inbound }
    }


# RemnaShop
msg-remnashop-main = <b><tg-emoji emoji-id="5920332557466997677">🛍</tg-emoji> RemnaShop { $version ->
[0] { space }
*[HAS] { $version }
}</b>

msg-remnashop-transactions = <b><tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Recent transactions</b>


# Backup
msg-backup-main =
    <b><tg-emoji emoji-id="6032745346390560408">💾</tg-emoji> Database auto-backup</b>

    <blockquote>
    • <b>Status</b>: { $enabled ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
    }
    • <b>Send to chat</b>: { $send_to_chat ->
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Enabled
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Disabled
    }
    • <b>Interval</b>:  { $interval_hours ->
    [one] every
    *[OTHER] every
    } { $interval_hours }h
    • <b>Number of files</b>: { $max_files }
    </blockquote>

msg-backup-set-interval =
    <b><tg-emoji emoji-id="5983150113483134607">🕐</tg-emoji> Backup interval</b>

    Current value: <b>{ $interval_hours }h</b>

    Enter the backup interval in hours (1 to 720).

msg-backup-set-max-files =
    <b><tg-emoji emoji-id="5805550320985578625">📁</tg-emoji> Number of files</b>

    Current value: <b>{ $max_files }</b>

    Enter how many backup files to keep (1 to 30). Old files will be deleted automatically.

msg-extra-main = <b><tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> Extra settings</b>

msg-extra-device-single =
    <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> <b>Single device deletion</b>

    Allows the user to delete a specific device from the list.

    <blockquote>
    <b>Status:</b> { $enabled -> 
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
    }
    <b>Cooldown:</b> { $cooldown -> 
        [0] { unknown }
        *[OTHER] { $cooldown }h
    }
    </blockquote>

    Enter a number to change the cooldown (in hours; 0 — no limit).

msg-extra-device-all =
    <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> <b>All devices deletion</b>

    Allows users to delete all devices with a single tap.

    <blockquote>
    <b>Status:</b> { $enabled -> 
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Enabled
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Disabled
    }
    <b>Cooldown:</b> { $cooldown -> 
        [0] { unknown }
        *[OTHER] { $cooldown }h
    }
    </blockquote>

    Enter a number to change the cooldown (in hours; 0 — no limit).

msg-extra-link-reset =
    <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> <b>Subscription reissue</b>

    Allows reissuing the connection link (invalidates the old one).

    <blockquote>
    <b>Status:</b> { $enabled -> 
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Enabled
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Disabled
    }
    <b>Cooldown:</b> { $cooldown -> 
        [0] { unknown }
        *[OTHER] { $cooldown }h
    }
    </blockquote>

    Enter a number to change the cooldown (in hours; 0 — no limit).

msg-extra-referral-reset =
    <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> <b>Referral link reset</b>

    Allows users to change their referral link.

    <blockquote>
    <b>Status:</b> { $enabled -> 
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Enabled
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Disabled
    }
    <b>Cooldown:</b> { $cooldown -> 
        [0] { unknown }
        *[OTHER] { $cooldown }h
    }
    </blockquote>

    Enter a number to change the cooldown (in hours; 0 — no limit).

msg-extra-trial-channel-guard =
    <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> <b>Auto-disable trial on channel unsubscribe</b>

    If a user unsubscribes from the required channel/group during the trial period, their subscription is automatically paused. After they subscribe again, access is restored if the trial has not expired yet.

    <blockquote>
    <b>Status:</b> { $enabled ->
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Enabled
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Disabled
    }
    </blockquote>

    Works only when the required channel/group subscription is enabled.

msg-extra-mini-app-reserve =
    <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> <b>Backup connect button when Mini App is active</b>

    A backup button that opens the subscription page in the browser is added under the main "Connect" button (which opens the Mini App). Useful in regions where the Telegram Mini App may be unavailable due to blocking.

    <blockquote>
    <b>Status:</b> { $enabled ->
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Enabled
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Disabled
    }
    </blockquote>

    Works only when the Mini App is enabled (BOT_MINI_APP).

msg-admins-main = <b><tg-emoji emoji-id="6030445631921721471">👮‍♂️</tg-emoji> Administrators</b>


# Menu editor
msg-menu-editor-main =
    <b><tg-emoji emoji-id="5776424837786374634">🎛</tg-emoji> Main menu button editor</b>

    Select a button to edit.

msg-menu-editor-button =
    <b><tg-emoji emoji-id="5776424837786374634">🎛</tg-emoji> Button configurator</b>

    <blockquote>
    • <b>Status</b>: { $is_active ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
        }
    • <b>Text</b>: { $text }
    • <b>Access</b>: { role }
    • <b>Visibility</b>: { $subscribers_only ->
        [1] <tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> Subscribers only
        *[0] <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> All users
        }
    • <b>Type</b>: { button-type }
    • <b>Color</b>: { $color ->
        [primary] Primary
        [success] Green
        [danger] Red
        *[OTHER] No color
        }
    { $type ->
        [TEXT] { empty }
       *[OTHER] • <b>Data</b>: { $payload }
    }
    </blockquote>

    Select an item to change.

msg-menu-editor-button-text =
    <b><tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Change button text</b>

    Enter the button text (maximum 32 characters) or a translation key.

msg-menu-editor-button-availability =
    <b><tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Change button access</b>

    Select the role that can access the button.

msg-menu-editor-button-type =
    <b><tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Change button type</b>

    Select the button type.

msg-menu-editor-button-payload =
    <b><tg-emoji emoji-id="6037475557082403885">📄</tg-emoji> Change button data</b>

    { $button_type ->
        [URL] Enter a link. It must start with <code>https://</code>.
        [COPY] Enter the text that will be copied to the clipboard when pressed.
        [WEB_APP] Enter a web app link. It must start with <code>https://</code>; <code>t.me</code> links are not supported.
        *[TEXT] Send a message (HTML is supported). You can attach a photo, video, file or sticker. Limit: up to 4096 characters without media, up to 1024 characters with media.
    }

msg-menu-editor-button-color =
    <b><tg-emoji emoji-id="5769635757211784031">🎨</tg-emoji> Change button color</b>

    Select the button color.


# Gateways
msg-gateways-main = <b><tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Payment systems</b>
msg-gateways-settings = <b><tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> { gateway-type } configuration</b>
msg-gateways-default-currency = <b><tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Default currency</b>
msg-gateways-placement = <b><tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Change position</b>

msg-gateways-field =
    <b><tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> { gateway-type } configuration</b>

    Enter a new value for { $field ->
        [display_name] the display name
       *[other] { $field }
    }.


# Referral
msg-referral-main =
    <b><tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Referral system</b>

    <blockquote>
    • <b>Status</b>: { $is_enable -> 
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
        }
    • <b>Reward type</b>: { reward-type }
    • <b>Number of levels</b>: { $referral_level }
    • <b>Accrual condition</b>: { accrual-strategy }
    • <b>Accrual form</b>: { reward-strategy }
    </blockquote>

    Select an item to change.

msg-referral-level =
    <b><tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Change level</b>

    Select the maximum referral level.

msg-referral-reward-type =
    <b><tg-emoji emoji-id="6037175527846975726">🎀</tg-emoji> Change reward type</b>

    Select a new reward type.
    
msg-referral-accrual-strategy =
    <b><tg-emoji emoji-id="6042011682497106307">📍</tg-emoji> Change accrual condition</b>

    Select when the reward will be credited.


msg-referral-reward-strategy =
    <b>⚖️ Change accrual form</b>

    Select how the reward is calculated.


msg-referral-reward-level = Level { $level }: { $value }{ $reward_strategy_type ->
    [AMOUNT] { $reward_type ->
        [POINTS] { space }{ $value -> 
            [one] point
            *[more] points
            }
        [EXTRA_DAYS] { space }extra { $value -> 
            [one] day
            *[more] days
            }
        *[OTHER] { $reward_type }
    }
    [PERCENT] % { $reward_type ->
        [POINTS] points
        [EXTRA_DAYS] extra days
        *[OTHER] { $reward_type }
    }
    *[OTHER] { $reward_strategy_type }
    }
    
msg-referral-reward =
    <b><tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Change reward</b>

    <blockquote>
    { $reward }
    </blockquote>

    { $reward_strategy_type ->
        [AMOUNT] Enter the number of { $reward_type ->
            [POINTS] points
            [EXTRA_DAYS] days
            *[OTHER] { $reward_type }
        }
        [PERCENT] Enter the percentage of { $reward_type ->
            [POINTS] <u>subscription price</u>
            [EXTRA_DAYS] <u>subscription duration</u>
            *[OTHER] { $reward_type }
        }
        *[OTHER] { $reward_strategy_type }
    } (format: level=value)


# Plans
msg-plans-main = <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Plans</b>

msg-plans-import = 
    <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Import plans</b>

    Send a JSON file to import.

msg-plans-export = 
    <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Export plans</b>

    Select plans to export.

msg-plan-configurator =
    <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Plan configurator</b>

    <blockquote>
    • <b>Name</b>: { $name }
    • <b>Type</b>: { plan-type } { $is_trial ->
    [1] (Trial)
    *[0] { space }
    }
    • <b>Access</b>: { availability-type }
    • <b>Status</b>: { $is_active -> 
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
        }
    </blockquote>
    
    <blockquote>
    • <b>Traffic limit</b>: { $is_unlimited_traffic -> 
        [1] { unlimited }
        *[0] { $traffic_limit }
        }
    • <b>Device limit</b>: { $is_unlimited_devices -> 
        [1] { unlimited }
        *[0] { $device_limit }
        }
    </blockquote>

    Select an item to change.

msg-plan-name =
    <b><tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Change name</b>

    { $name ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $name }
    </blockquote>
    }

    Enter a unique plan name or a translation key (maximum 32 characters).

msg-plan-description =
    <b><tg-emoji emoji-id="6030784887093464891">💬</tg-emoji> Change description</b>

    { $description ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $description }
    </blockquote>
    }

    Enter a new plan description or a translation key.

msg-plan-tag =
    <b><tg-emoji emoji-id="6043896193887506430">📌</tg-emoji> Change tag</b>

    { $tag ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $tag }
    </blockquote>
    }

    Enter a new plan tag (only uppercase Latin letters, digits and underscores).

msg-plan-type =
    <b><tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Change type</b>

    Select a new plan type. Use the "Trial" button to offer this plan as a trial.

msg-plan-availability =
    <b><tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Change availability</b>

    Select the plan availability.

msg-plan-traffic =
    <b><tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Change traffic limit and reset strategy</b>

    Enter the new plan traffic limit (in GB) and select its reset strategy.

msg-plan-devices =
    <b><tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Change device limit</b>

    Enter the new plan device limit.

msg-plan-durations =
    <b><tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Plan durations</b>

    Select a duration to change its price.

msg-plan-duration =
    <b><tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Add plan duration</b>

    Enter the new duration (in days).

msg-plan-prices =
    <b><tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> Change duration prices ({ $value ->
            [0] { unlimited }
            *[OTHER] { unit-day }
        })</b>

    Select the currency whose price you want to change.

msg-plan-price =
    <b><tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> Change price for duration ({ $value ->
            [0] { unlimited }
            *[OTHER] { unit-day }
        })</b>

    Enter the new price for currency { $currency }.

msg-plan-allowed-users = 
    <b><tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Change allowed users list</b>

    Enter a user ID or email to add to the list.

msg-plan-squads =
    <b><tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Squads</b>

    { $internal_squads ->
    [0] { space }
    *[HAS] <b><tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Internal</b>: { $internal_squads }
    }

    { $external_squad ->
    [0] { space }
    *[HAS] <b><tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> External</b>: { $external_squad }
    }

msg-plan-internal-squads =
    <b><tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Change internal squad list</b>

    Select which internal groups will be assigned to this plan.

msg-plan-external-squads =
    <b><tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> Change external squad</b>

    Select which external group will be assigned to this plan.


# Notifications
msg-notifications-main = <b><tg-emoji emoji-id="6039486778597970865">🔔</tg-emoji> Notification settings</b>
msg-notifications-user = <b><tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> User notifications</b>
msg-notifications-system = <b><tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> System notifications</b>

msg-notifications-system-type = 
    <b><tg-emoji emoji-id="6039486778597970865">🔔</tg-emoji> { notification-type }</b>

    <blockquote>
    • <b>Status</b>: { $is_active -> 
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }
    • <b>Route</b>: { $has_route -> 
    [0] { unknown }
    *[HAS] { NUMBER($chat_id, useGrouping: 0) }{ $thread_id ->
        [0] { space }
        *[HAS] :{ NUMBER($thread_id, useGrouping: 0) }
        }
    }
    </blockquote>

msg-notifications-system-route = 
    <b><tg-emoji emoji-id="6048723247501938454">📡</tg-emoji> Route: { notification-type }</b>

    <blockquote>
    • <b>Chat ID</b>: { $chat_id ->
        [0] { unknown }
        *[HAS] <code>{ NUMBER($chat_id, useGrouping: 0) }</code>
        }
    • <b>Thread ID</b>: { $thread_id ->
        [0] { unknown }
        *[HAS] <code>{ NUMBER($thread_id, useGrouping: 0) }</code>
        }
    </blockquote>

    If the chat ID is not set, the notification will be sent to private messages.
    
    If the thread ID is not set, the notification will be sent to the chat.


msg-notifications-system-default-route =
    <b><tg-emoji emoji-id="6048723247501938454">📡</tg-emoji> Default route</b>

    <blockquote>
    • <b>Chat ID</b>: { $chat_id ->
        [0] { unknown }
        *[HAS] <code>{ NUMBER($chat_id, useGrouping: 0) }</code>
        }
    • <b>Thread ID</b>: { $thread_id ->
        [0] { unknown }
        *[HAS] <code>{ NUMBER($thread_id, useGrouping: 0) }</code>
        }
    </blockquote>

    The route applies to all system notifications that don't have their own route.

    If the chat ID is not set, the notification will be sent to private messages.

    If the thread ID is not set, the notification will be sent to the chat.


msg-notifications-system-route-chat-id =
    <b><tg-emoji emoji-id="6030784887093464891">💬</tg-emoji> Change Chat ID</b>

    Enter the group ID (for example: <code>-1001234567891</code>).

msg-notifications-system-route-thread-id =
    <b><tg-emoji emoji-id="5805550320985578625">📁</tg-emoji> Change Thread ID</b>

    Enter the thread ID (enter <code>0</code> to reset).


# Subscription
msg-subscription-main = <b><tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Subscription</b>
msg-subscription-plans = <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Select a plan</b>
msg-subscription-new-success = To start using our service, press the <code>`{ btn-subscription.connect }`</code> button and follow the instructions!
msg-subscription-renew-success = Your subscription has been extended by { $added_duration }.

msg-subscription-plan = 
    <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Plan available via link</b>
    
    The plan <b>{ $name }</b> is available to you via the link. Press the button below to choose the duration and payment method.

    { $description ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $description }
    </blockquote>
    }

    { $purchase_type ->
    [RENEW] <i><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Your current subscription will be <u>extended</u> by the selected period.</i>
    [CHANGE] <i><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Your current subscription will be <u>replaced</u> with this plan without recalculating the remaining time.</i>
    *[OTHER] { empty }
    }
    
msg-subscription-details =
    <b>{ $plan }</b>:
    <blockquote>
    { $description ->
    [0] { empty }
    *[HAS]
    { $description }
    }

    • <b>Traffic limit</b>: { $traffic }
    • <b>Device limit</b>: { $devices }
    { $period ->
    [0] { empty }
    *[HAS] • <b>Duration</b>: { $period }
    }
    { $final_amount ->
    [0] { empty }
    *[HAS] • <b>Price</b>: { frg-payment-amount }
    }
    </blockquote>
    
    { $discount_percent ->
    [0] { empty }
    *[HAS]
    <blockquote>
    <i>Prices include { $is_personal_discount ->
        [1] your personal discount { $discount_percent }%
        *[0] a one-time discount { $discount_percent }%
        }</i>
    </blockquote>
    }

msg-subscription-duration =
    <b><tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Select duration</b>

    { msg-subscription-details }

    { $plan_is_modified ->
    [1] <i>ℹ️ The plan terms have changed since your last purchase — current details are shown above.</i>
    *[0] { "" }
    }

msg-subscription-payment-method =
    <b><tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Select payment method</b>

    { msg-subscription-details }

    { $plan_is_modified ->
    [0] { empty }
    *[MODIFIED] <i>ℹ️ The plan terms have changed since your last purchase — current details are shown above.</i>
    }

msg-subscription-confirm =
    <b><tg-emoji emoji-id="5920332557466997677">🛒</tg-emoji> Confirm { $purchase_type ->
    [RENEW] subscription renewal
    [CHANGE] subscription change
    *[OTHER] subscription purchase
    }</b>

    { msg-subscription-details }

    { $purchase_type ->
    [RENEW] <i><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Your current subscription will be <u>extended</u> by the selected period.</i>
    [CHANGE] <i><tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> Your current subscription will be <u>replaced</u> with the selected one without recalculating the remaining time.</i>
    *[OTHER] { empty }
    }

    { $plan_is_modified ->
    [0] { empty }
    *[MODIFIED] <i>ℹ️ The plan terms have changed since your last purchase — current details are shown above.</i>
    }

msg-subscription-trial =
    <b><tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Trial subscription received successfully!</b>

    { msg-subscription-new-success }

msg-subscription-success =
    <b><tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Payment successful!</b>

    { $purchase_type ->
    [NEW] { msg-subscription-new-success }
    [RENEW] { msg-subscription-renew-success }
    [CHANGE] { msg-subscription-change-success }
    *[OTHER] { $purchase_type }
    }

msg-subscription-change-success = 
    Your subscription has been changed.

    <b>{ $plan_name }</b>
    { frg-subscription }

msg-subscription-failed = 
    <b><tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> An error occurred!</b>

    Don't worry, support has already been notified and will contact you shortly. We apologize for the inconvenience.


# Importer
msg-importer-main = <b><tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Import users</b>

msg-importer-from-xui =
    <b><tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Import users (3X-UI)</b>
    
    { $has_exported -> 
    [1]
    <b><tg-emoji emoji-id="6032850693348399258">🔍</tg-emoji> Found</b>:
    <blockquote>
    Total users: { $total }
    With active subscription: { $active }
    With expired subscription: { $expired }
    </blockquote>
    *[0]
    All <b>active</b> users with a <b>numeric</b> email are imported.

    It is recommended to disable in advance any users whose email field has no Telegram ID. The operation may take a considerable amount of time depending on the number of users.

    Send the database file (in .db format).
    }

msg-importer-squads =
    <b><tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Internal squad list</b>

    Select which internal groups will be available to imported users.

msg-importer-import-completed =
    <b><tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> User import completed</b>
    
    <b><tg-emoji emoji-id="6050643982646513651">📃</tg-emoji> Information</b>:
    <blockquote>
    • <b>Total users</b>: { $total_count }
    • <b>Successfully imported</b>: { $success_count }
    • <b>Failed to import</b>: { $failed_count }
    </blockquote>

msg-importer-sync-panel =
    <b><tg-emoji emoji-id="5769248574499983619">🌀</tg-emoji> Sync: panel → bot</b>

    Goes through all users in RemnaWave. If a user is missing in the bot, creates them and imports their subscription. If a user exists in the bot without a subscription, imports the subscription from the panel. If a user exists in the bot with a subscription, updates the data.

msg-importer-sync-bot =
    <b><tg-emoji emoji-id="6030400221232501136">🤖</tg-emoji> Sync: bot → panel</b>

    Goes through all bot users. If a user has no subscription in the bot, skips them and the panel is not affected. If a subscription exists but the user is missing in the panel, creates them. If the user exists in the panel, updates the data.

msg-importer-sync-panel-completed =
    <b><tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Panel → bot synchronization completed</b>

    <b><tg-emoji emoji-id="6050643982646513651">📃</tg-emoji> Information</b>:
    <blockquote>
    Total users in panel: { $total_panel_users }
    Total users in bot: { $total_bot_users }

    New users: { $added_users }
    Subscriptions added: { $added_subscription }
    Subscriptions updated: { $updated }

    Synchronization errors: { $errors }
    </blockquote>

msg-importer-sync-bot-completed =
    <b><tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Bot → panel synchronization completed</b>

    <b><tg-emoji emoji-id="6050643982646513651">📃</tg-emoji> Information</b>:
    <blockquote>
    Total users in bot: { $total_bot_users }

    Updated in panel: { $updated }
    Recreated in panel: { $recreated }
    
    Without subscription (skipped): { $skipped_no_subscription }
    Synchronization errors: { $errors }
    </blockquote>


# Promocodes
msg-promocodes-main = <b><tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Promocodes</b>

msg-promocode-configurator =
    <b><tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Promocode configurator</b>

    <blockquote>
    • <b>Code</b>: <code>{ $code }</code>
    • <b>Type</b>: { promocode-type }
    • <b>Access</b>: { availability-type }
    • <b>Status</b>: { $is_active ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
        }
    • <b>Reactivation</b>: { $is_reusable ->
        [1] Allowed
        *[0] Forbidden
        }
    </blockquote>

    <blockquote>
    • <b>Reward</b>: { $reward }
    • <b>Valid until</b>: { $expires }
    • <b>Activation limit</b>: { $max_activations }
    </blockquote>

    Select an item to change.

msg-promocode-input-code =
    <b><tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Change code</b>

    { $code ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $code }
    </blockquote>
    }

    Send your unique code (3 to 16 characters).

msg-promocode-select-type =
    <b><tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Change reward type</b>

    Select the reward type.

msg-promocode-input-reward =
    <b><tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Change reward</b>

    { $reward ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $reward }
    </blockquote>
    }

    { $promocode_type ->
    [DURATION] Enter the number of <b>days</b> to add to the user's subscription on activation (the value <code>0</code> makes the subscription unlimited).
    [TRAFFIC] Enter the number of <b>gigabytes (GB)</b> to add to the subscription traffic limit (the value <code>0</code> makes traffic unlimited).
    [DEVICES] Enter the number of <b>devices</b> to add to the subscription limit (the value <code>0</code> removes the device limit).
    [PERSONAL_DISCOUNT] Enter the <b>personal discount</b> size in percent — from 1 to 100.
    [PURCHASE_DISCOUNT] Enter the <b>purchase discount</b> size in percent — from 1 to 100.
    *[OTHER] Enter the reward value (an integer).
    }

msg-promocode-select-plan =
    <b><tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Change plan</b>

    Select a plan.

msg-promocode-select-plan-duration =
    <b><tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Change duration</b>

    Select the plan duration.

msg-promocode-select-availability =
    <b><tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Change availability</b>

    Select the promocode availability.

msg-promocode-input-expires =
    <b><tg-emoji emoji-id="5891211339170326418">⌛</tg-emoji> Valid until</b>

    { $expires ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $expires }
    </blockquote>
    }

    Enter a date "DD.MM.YYYY" (or with time "DD.MM.YYYY HH:MM"), or a number — days since creation.

    Time is in UTC.

msg-promocode-input-max-activations =
    <b><tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Change activation limit</b>

    { $max_activations ->
    [0] { space }
    *[HAS]
    <blockquote>
    { $max_activations }
    </blockquote>
    }

    Enter the maximum number of activations.

msg-promocode-input =
    <b><tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Promocode</b>

    Enter the promocode.

msg-promocode-confirm =
    <b><tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Promocode <code>{ $promo_code }</code></b>

    <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> You will get: { $reward_type ->
        [DURATION] { $reward ->
            [0] your current subscription will become <b>unlimited</b>.
            *[OTHER] <b>{ $reward } { $reward ->
                [one] day
                *[more] days
            }</b> added to your current subscription term.
        }
        [TRAFFIC] { $reward ->
            [0] <b>unlimited traffic</b> in your current subscription.
            *[OTHER] <b>{ $reward } GB</b> added to the traffic limit.
        }
        [DEVICES] { $reward ->
            [0] <b>unlimited devices</b> in your current subscription.
            *[OTHER] <b>{ $reward } { $reward ->
                [one] device
                *[more] devices
            }</b> added to the device limit.
        }
        [SUBSCRIPTION] a <b>new subscription plan</b>.
        [PERSONAL_DISCOUNT] a permanent <b>{ $reward }% discount</b> on all purchases.
        [PURCHASE_DISCOUNT] a <b>{ $reward }% discount</b> on your next purchase.
        *[OTHER] a reward for your account.
    }
    
    { $show_reset_warning ->
        [1] <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>The bonus is valid until your next subscription renewal — on renewal the limit returns to the plan value.</i>
       *[0] { space }
    }
    { $will_replace_subscription ->
        [1] <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> <i>You already have an active subscription. It will be replaced with the new plan, and the remaining days and traffic will be reset.</i>
       *[0] { space }
    }

    Press <b>Confirm</b> to activate.


# Ad Links
msg-ad-links-main = <b><tg-emoji emoji-id="6032949275732742941">🎯</tg-emoji> Ad links</b>

msg-ad-link-configurator =
    <b><tg-emoji emoji-id="6032949275732742941">🎯</tg-emoji> Ad link configurator</b>

    <blockquote>
    • <b>Name</b>: { $name ->
        [0] not set
        *[HAS] { $name }
    }
    • <b>Code</b>: { $code ->
        [0] not set
        *[HAS] <code>{ $code }</code>
    }
    • <b>Status</b>: { $is_active ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
    }
    </blockquote>

    Select an item to change.

msg-ad-link-name =
    <b><tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Link name</b>

    { $name ->
    [0] { space }
    *[HAS]
    <blockquote>{ $name }</blockquote>
    }

    Enter the ad campaign name.

msg-ad-link-code =
    <b><tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Link code</b>

    Current: <code>{ $code }</code>

    Send your unique code or press the button.

msg-ad-link-stats =
    <b><tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Statistics: { $name }</b>

    <blockquote>
    • <b>Registrations</b>: { $registrations }
    • <b>Trials</b>: { $trials }
    • <b>Purchases</b>: { $buyers }

    • <b>Conversion: registration → purchase</b>: { $reg_to_buy_rate }%
    • <b>Conversion: trial → purchase</b>: { $trial_to_buy_rate }%
    </blockquote>

    <blockquote>
    { $revenue_lines }
    </blockquote>

msg-profile-email-input =
    <b><tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> { $has_email ->
        [0] Add email
        *[other] Change email
    }</b>

    Send your email in a message. A confirmation code will be sent to it.

msg-profile-email-code =
    <b><tg-emoji emoji-id="6028346797368283073">✈️</tg-emoji> Email confirmation</b>

    The code was sent to <code>{ $pending_email }</code>. Send it in a message to complete linking.

    <blockquote><i>If the email didn't arrive, check your Spam folder or request the code again.</i></blockquote>

msg-user-email-set =
    <b><tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> User email</b>

    { $email ->
        [0] <i>No email set.</i>
        *[other] <b>Current email:</b> <code>{ $email }</code>
    }

    Send a new email in a message to set or change it.

msg-user-email-options =
    <b><tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> User email</b>

    { $email ->
        [0] <i>No email set. Set one to be able to send emails.</i>
        *[other] <b>Current email:</b> <code>{ $email }</code>
    }

    Select an action.

msg-user-password-reset =
    <b><tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> Password reset</b>

    User: <code>{ $email }</code>

    Send a new password in a message (8 to 256 characters). All of the user's active sessions will be terminated. The message with the password will be deleted automatically.

msg-user-email-custom =
    <b><tg-emoji emoji-id="6039573425268201570">📨</tg-emoji> Custom email</b>

    Recipient: <code>{ $email }</code>

    Send the email content as a text or HTML message (HTML is supported, up to 4096 characters). The text will be placed in the center of the email, with a button to the Telegram bot added below it.
