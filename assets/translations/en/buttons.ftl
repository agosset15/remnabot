btn-back =
    .general = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Back
    .menu = <tg-emoji emoji-id="5960671702059848143">↩️</tg-emoji> Main menu
    .menu-return = <tg-emoji emoji-id="5960671702059848143">↩️</tg-emoji> Back to main menu
    .dashboard = <tg-emoji emoji-id="5960671702059848143">↩️</tg-emoji> Back to dashboard
    .referrals = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Back to referrals

btn-common =
    .notification-close = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Close
    .devices-empty = <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> You have no connected devices
    .cancel = Cancel
    .next = <tg-emoji emoji-id="5773626993010546707">▶️</tg-emoji> Next
    .prev = <tg-emoji emoji-id="5960671702059848143">◀️</tg-emoji> Back

    .squad-choice = { $selected -> 
    [1] 🔘
    *[0] ⚪
    } { $name }

    .duration = <tg-emoji emoji-id="5891211339170326418">⌛</tg-emoji> { $value ->
    [0] { unlimited }
    *[OTHER] { unit-day }
    }

btn-devices =
    .delete-all = <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> Delete all devices
    .reissue = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Reissue subscription
    .confirm-delete = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Yes, delete
    .confirm-reissue = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Yes, reset
    .cancel-reissue = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> No

    .item = { $platform_icon } { $platform } { $device_model -> 
    [0] { space }
    *[HAS] ({ $device_model }){ space }
    }— { $created_at }

btn-backup =
    .active-toggle = { $enabled ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
    }
    .set-interval = <tg-emoji emoji-id="5983150113483134607">🕐</tg-emoji> Interval
    .set-max-files = <tg-emoji emoji-id="5805550320985578625">📁</tg-emoji> Number of files
    .send-toggle = { $send_to_chat ->
        [1] <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Send to chat: on
        *[0] <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Send to chat: off
    }
    .backup-assets = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Run assets backup
    .backup-db = <tg-emoji emoji-id="5778672437122045013">🗄</tg-emoji> Run database backup
    
btn-remnashop-info =
    .release-latest = <tg-emoji emoji-id="6037397706505195857">👀</tg-emoji> View
    .how-upgrade = <tg-emoji emoji-id="6030848053177486888">❓</tg-emoji> How to update
    .github = <tg-emoji emoji-id="6034923938486684992">⭐</tg-emoji> GitHub
    .telegram = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Telegram
    .donate = <tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> Support the developer
    .docs = <tg-emoji emoji-id="6050643982646513651">📖</tg-emoji> Documentation

btn-requirement =
    .rules-accept = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Accept the rules
    .channel-join = <tg-emoji emoji-id="5938368005611195877">❤️</tg-emoji> Go to channel
    .channel-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Confirm

btn-menu =
    .trial = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> TRY FOR FREE
    .trial-paid = <tg-emoji emoji-id="6028205772117118673">🚀</tg-emoji> TRY FOR { $trial_price }
    .connect = <tg-emoji emoji-id="6028205772117118673">🚀</tg-emoji> Connect
    .connect-reserve = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Connect (backup)
    .devices = <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Devices
    .subscription = <tg-emoji emoji-id="5886583490434044162">💳</tg-emoji> Subscription
    .invite = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Invite
    .support = <tg-emoji emoji-id="6032636795387121097">🆘</tg-emoji> Support
    .web-cabinet = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Web account
    .dashboard = <tg-emoji emoji-id="5776424837786374634">🛠</tg-emoji> Dashboard

    .connect-not-available =
    <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji> { $status ->
    [LIMITED] TRAFFIC LIMIT EXCEEDED
    [EXPIRED] SUBSCRIPTION EXPIRED
    *[OTHER] YOUR SUBSCRIPTION IS NOT WORKING
    } <tg-emoji emoji-id="6030563507299160824">⚠️</tg-emoji>

btn-profile =
    .email-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Confirm email
    .email-change = <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Change email
    .email-add = <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Link email
    .email = <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Email
    .code-resend = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Resend code

btn-invite =
    .about = <tg-emoji emoji-id="6030848053177486888">❓</tg-emoji> About the reward
    .copy = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Copy link
    .send = <tg-emoji emoji-id="6039391666547201160">📩</tg-emoji> Invite
    .qr = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> QR code
    .withdraw-points = <tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Exchange points
    .reset-referral = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Reset referral link

btn-dashboard =
    .statistics = <tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Statistics
    .users = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Users
    .broadcast = <tg-emoji emoji-id="6021418126061605425">📢</tg-emoji> Broadcast
    .promocodes = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Promocodes
    .access = <tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Access mode
    .remnawave = <tg-emoji emoji-id="5463406057885821287">🌊</tg-emoji> RemnaWave
    .remnashop = <tg-emoji emoji-id="5920332557466997677">🛍</tg-emoji> RemnaShop
    .transactions = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Transactions
    .importer = <tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Import users

btn-statistics =
    .users = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Users
    .subscriptions = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Subscriptions
    .transactions = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Transactions
    .promocodes = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Promocodes
    .referrals = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Referrals

    .subscription-page =
    { $page ->
        [0] { $is_current ->
            [1] [ Overall statistics ]
            *[0] Overall statistics
        }
        *[OTHER] { $is_current ->
            [1] [ { $plan_name } ]
            *[0] { $plan_name }
        }
    }

    .transaction-page =
    { $page ->
        [0] { $is_current ->
            [1] [ Overall statistics ]
            *[0] Overall statistics
        }
        *[OTHER] { $is_current ->
            [1] [ { gateway-type } ]
            *[0] { gateway-type }
        }
    }

btn-users =
    .search = <tg-emoji emoji-id="6032850693348399258">🔍</tg-emoji> Search user
    .recent-registered = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Recently registered
    .recent-activity = <tg-emoji emoji-id="6039614175917903752">📝</tg-emoji> Recently active
    .blacklist = <tg-emoji emoji-id="5938215362473496448">🚫</tg-emoji> Blacklist
    .unblock-all = <tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Unblock all
    .blacklist-view = <tg-emoji emoji-id="5766994197705921104">🗒️</tg-emoji> List of blocked users
    .blacklist-block = <tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Block by ID
    .blacklist-sources = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Auto-updated lists
    .blacklist-sources-sync = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Synchronize
    .blacklist-block-clear = <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> Clear ID list

    .blacklist-source = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> { $source }

btn-user =
    .email = <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Email
    .email-purchase = <tg-emoji emoji-id="5776182936638329359">📧</tg-emoji> Email: purchase
    .email-connect = <tg-emoji emoji-id="5776182936638329359">📧</tg-emoji> Email: link Telegram
    .email-custom = <tg-emoji emoji-id="6039573425268201570">📨</tg-emoji> Email: custom text
    .email-set = { $has_email ->
        [0] <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Set email
        *[other] <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Change email
    }
    .email-clear = <tg-emoji emoji-id="6039522349517115015">🗑</tg-emoji> Delete email
    .password-reset = <tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> Reset password
    .discount = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Discount
    .discount-personal = <tg-emoji emoji-id="6035084557378654059">👤</tg-emoji> Personal discount
    .discount-purchase = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> On next purchase
    .points = <tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Points
    .statistics = <tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Statistics
    .referrals = <tg-emoji emoji-id="5938196735200333756">👪</tg-emoji> Referrals
    .message = <tg-emoji emoji-id="6039391666547201160">📩</tg-emoji> Message
    .role = <tg-emoji emoji-id="6030445631921721471">👮‍♂️</tg-emoji> Role
    .transactions = <tg-emoji emoji-id="6050643982646513651">🧾</tg-emoji> Transactions
    .give-access = 🔑 Plan access
    .current-subscription = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Current subscription
    .subscription-traffic-limit = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Traffic limit
    .subscription-device-limit = <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Device limit
    .subscription-expire-time = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Expiration time
    .subscription-squads = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Squads
    .subscription-traffic-reset = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Reset traffic
    .subscription-devices = <tg-emoji emoji-id="5766994197705921104">🗒️</tg-emoji> Device list
    .subscription-url = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Copy link
    .subscription-delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Delete
    .subscription-reissue = <tg-emoji emoji-id="6030657343744644592">♻️</tg-emoji> Reissue
    .message-preview = <tg-emoji emoji-id="6037397706505195857">👀</tg-emoji> Preview
    .message-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Send
    .referral-reset = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Reset referral link
    .sync = <tg-emoji emoji-id="5769248574499983619">🌀</tg-emoji> Synchronize
    .sync-remnawave = 🌊 Use Remnawave data
    .sync-remnashop = <tg-emoji emoji-id="5920332557466997677">🛍</tg-emoji> Use Remnashop data
    .give-subscription = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Give subscription
    .subscription-internal-squads = <tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Internal squads
    .subscription-external-squads = <tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> External squad

    .allowed-plan-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    } { $plan_name }

    .subscription-active-toggle = { $is_active ->
    [1] 🔴 Disable
    *[0] 🟢 Enable
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
    [1] <tg-emoji emoji-id="6050677620830376838">🧪</tg-emoji> Trial: available
    *[0] <tg-emoji emoji-id="6050677620830376838">🧪</tg-emoji> Trial: unavailable
    }

    .block = { $is_blocked ->
    [1] <tg-emoji emoji-id="6037496202990194718">🔓</tg-emoji> Unblock
    *[0] <tg-emoji emoji-id="6037249452824072506">🔒</tg-emoji> Block
    }

btn-broadcast =
    .list = <tg-emoji emoji-id="5766994197705921104">🗒️</tg-emoji> All broadcasts
    .all = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Everyone
    .plan = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> By plan
    .subscribed = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> With subscription
    .unsubscribed = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Without subscription
    .expired = <tg-emoji emoji-id="5891211339170326418">⌛</tg-emoji> Expired
    .trial = ✳️ With trial
    .content = <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> Edit content
    .buttons = ✳️ Edit buttons
    .preview = <tg-emoji emoji-id="6037397706505195857">👀</tg-emoji> Preview
    .confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Start broadcast
    .refresh = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Refresh data
    .cancel = <tg-emoji emoji-id="5891184096192763888">⛔</tg-emoji> Stop broadcast
    .delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Delete sent messages

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
    .subscription = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Buy subscription
    .promocode = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Activate promocode
    .invite = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Invite
    .subscription-renew = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Renew subscription
    .user-profile = <tg-emoji emoji-id="6035084557378654059">👤</tg-emoji> Go to user
    .referrer-profile = <tg-emoji emoji-id="5891207662678317861">🤝</tg-emoji> Go to referrer
    .contact-support = <tg-emoji emoji-id="6039391666547201160">📩</tg-emoji> Contact support
    .provider-login = 🔑 Go to provider

btn-promocodes =
    .save = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Save
    .create = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Create promocode
    .confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Create promocode
    .delete = <tg-emoji emoji-id="6039522349517115015">🗑️</tg-emoji> Delete
    .regenerate = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Regenerate
    .code = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Code
    .type = <tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Reward type
    .availability = <tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Access
    .reward = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Reward
    .plan = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Plan
    .expires = <tg-emoji emoji-id="5891211339170326418">⌛</tg-emoji> Expiration
    .max-activations = <tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Activation limit
    .reset = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Reset

    .plan-duration = { $days -> 
        [one] { $days } day
        *[more] { $days } days
    }

    .item = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> { $code } — { promocode-type }

    .active-toggle = { $is_active ->
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }

    .reusable-toggle = <tg-emoji emoji-id="6030657343744644592">🔁</tg-emoji> { $is_reusable ->
    [1] Repeatable: yes
    *[0] Repeatable: no
    }

btn-access =
    .mode = { access-mode }
    .conditions = <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> Access conditions
    .rules = ✳️ Rules acceptance
    .channel = ❇️ Channel subscription

    .payments-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Payments

    .registration-toggle = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } Registration

    .condition-toggle = { $enabled ->
    [1] 🔘 Enabled
    *[0] ⚪ Disabled
    }

btn-remnashop =
    .admins = <tg-emoji emoji-id="6030445631921721471">👮‍♂️</tg-emoji> Administrators
    .gateways = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Payment systems
    .referral = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Referral system
    .advertising = <tg-emoji emoji-id="6032949275732742941">🎯</tg-emoji> Advertising
    .plans = <tg-emoji emoji-id="5884479287171485878">📦</tg-emoji> Plans
    .notifications = <tg-emoji emoji-id="6039486778597970865">🔔</tg-emoji> Notifications
    .logs = <tg-emoji emoji-id="6037475557082403885">📄</tg-emoji> Logs
    .menu-editor = <tg-emoji emoji-id="5776424837786374634">🎛</tg-emoji> Main menu editor
    .backup = <tg-emoji emoji-id="6032745346390560408">💾</tg-emoji> Backup
    .extra = <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> Extra settings

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
    } Device deletion

    .device-all = { $enabled -> 
        [1] 🟢
        *[0] 🔴
    } All devices deletion

    .link-reset = { $enabled -> 
        [1] 🟢
        *[0] 🔴
    } Subscription reissue
    .referral-reset = { $enabled -> 
        [1] 🟢
        *[0] 🔴
    } Referral link reset

    .trial-channel-guard = { $enabled ->
        [1] 🟢
        *[0] 🔴
    } Auto-disable trial

    .mini-app-reserve = { $enabled ->
        [1] 🟢
        *[0] 🔴
    } Backup connect button

    .birthday-greeting = { $enabled ->
        [1] 🟢
        *[0] 🔴
    } Birthday greeting

    .toggle = { $enabled ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
    }

btn-menu-editor =
    .text = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Text
    .availability = <tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Access
    .type = <tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Type
    .payload = <tg-emoji emoji-id="6037475557082403885">📄</tg-emoji> Data
    .color = <tg-emoji emoji-id="5769635757211784031">🎨</tg-emoji> Color
    .confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Save
    .color-default = No color
    .color-primary = Primary
    .color-success = Green
    .color-danger = Red

    .button = { $is_active ->
        [1] 🟢
        *[0] 🔴
    } { $text }

    .active-toggle = { $is_active ->
        [1] 🟢 Enabled
        *[0] 🔴 Disabled
    }

    .subscribers-only-toggle = { $subscribers_only ->
        [1] <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> With subscription
        *[0] <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Everyone
    }

btn-gateway =
    .title = { gateway-type }
    .setting = { $field }
    .display-name = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Display name
    .webhook-copy = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Copy webhook
    .test = 🐞 Test
    .default-currency = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Default currency
    .placement = <tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Change position
    .field-reset = <tg-emoji emoji-id="6030657343744644592">♻️</tg-emoji> Reset value

    .active-toggle = { $is_active ->
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }

    .default-currency-choice = { $enabled ->
    [1] 🔘
    *[0] ⚪
    } { $symbol } { $currency }

btn-referral =
    .level = <tg-emoji emoji-id="5924498929147189381">🔢</tg-emoji> Level
    .reward-type = <tg-emoji emoji-id="6037175527846975726">🎀</tg-emoji> Reward type
    .accrual-strategy = <tg-emoji emoji-id="6042011682497106307">📍</tg-emoji> Accrual condition
    .reward-strategy = ⚖️ Accrual form
    .reward = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Reward
    
    .active-toggle = { $is_enable -> 
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }

    .level-choice = { $type -> 
    [1] <tg-emoji emoji-id="5794164805065514131">1️⃣</tg-emoji>
    [2] <tg-emoji emoji-id="5794085322400733645">2️⃣</tg-emoji>
    [3] <tg-emoji emoji-id="5794280000383358988">3️⃣</tg-emoji>
    *[OTHER] { $type }
    }

    .reward-choice = { $type -> 
    [POINTS] <tg-emoji emoji-id="6037083366438737901">💎</tg-emoji> Points
    [EXTRA_DAYS] <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Days
    *[OTHER] { $type }
    }

    .accrual-strategy-choice = { $type -> 
    [ON_FIRST_PAYMENT] <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> First payment
    [ON_EACH_PAYMENT] <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Every payment
    *[OTHER] { $type }
    }

    .reward-strategy-choice = { $type -> 
    [AMOUNT] 🔸 Fixed
    [PERCENT] 🔹 Percentage
    *[OTHER] { $type }
    }

btn-notifications =
    .user = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> User
    .system = <tg-emoji emoji-id="6032742198179532882">⚙️</tg-emoji> System
    .route = <tg-emoji emoji-id="6048723247501938454">📡</tg-emoji> Route
    .default-route = <tg-emoji emoji-id="6048723247501938454">📡</tg-emoji> Default route
    .chat-id = <tg-emoji emoji-id="6030784887093464891">💬</tg-emoji> Change chat
    .thread-id = <tg-emoji emoji-id="5805550320985578625">📁</tg-emoji> Change thread
    .route-clear = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Delete route
    
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
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }

btn-plans =
    .save = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Save
    .create = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Create plan
    .create-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Create plan
    .delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Delete
    .name = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Name
    .description = <tg-emoji emoji-id="6030784887093464891">💬</tg-emoji> Description
    .description-remove = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Remove current description
    .tag = <tg-emoji emoji-id="6043896193887506430">📌</tg-emoji> Tag
    .tag-remove = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Remove current tag
    .type = <tg-emoji emoji-id="6030425896546996257">🔖</tg-emoji> Type
    .availability = <tg-emoji emoji-id="5890925363067886150">✴️</tg-emoji> Access
    .durations-prices = <tg-emoji emoji-id="5891211339170326418">⏳</tg-emoji> Durations and <tg-emoji emoji-id="5769126056262898415">💰</tg-emoji> Prices
    .traffic = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Traffic
    .devices = <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Devices
    .allowed = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Allowed users
    .squads = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Squads
    .internal-squads = <tg-emoji emoji-id="5884332803016891855">⏺️</tg-emoji> Internal squads
    .external-squads = <tg-emoji emoji-id="5884089033558070257">⏹️</tg-emoji> External squad
    .duration-add = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Add duration
    .price-choice = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> { $price } { $currency }
    .export = <tg-emoji emoji-id="5805506958995758422">📤</tg-emoji> Export
    .import = <tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Import
    .exporting = <tg-emoji emoji-id="5805506958995758422">📤</tg-emoji> Export
    .importing = <tg-emoji emoji-id="5805382340519664323">📥</tg-emoji> Import
    .url = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Copy plan link

    .trial = { $is_trial ->
    [1] 🔘
    *[0] ⚪
    } Trial 

    .export-choice = { $selected ->
    [1] 🔘
    *[0] ⚪
    } { $name }

    .title = { $is_active ->
    [1] 🟢
    *[0] 🔴 
    } { $name }

    .active-toggle = { $is_active -> 
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }
    
    .type-choice = { $type -> 
    [TRAFFIC] <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Traffic
    [DEVICES] <tg-emoji emoji-id="5771652845652677093">📱</tg-emoji> Devices
    [BOTH] <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Traffic + devices
    [UNLIMITED] <tg-emoji emoji-id="6048407885233263063">♾️</tg-emoji> Unlimited
    *[OTHER] { $type }
    }

    .availability-choice = { $type -> 
    [ALL] <tg-emoji emoji-id="5776233299424843260">🌍</tg-emoji> For everyone
    [NEW] 🌱 For new users
    [EXISTING] <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> For customers
    [INVITED] <tg-emoji emoji-id="5776182936638329359">✉️</tg-emoji> For invited users
    [ALLOWED] <tg-emoji emoji-id="6037249452824072506">🔐</tg-emoji> For allowed users
    [LINK] <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> By link
    *[OTHER] { $type }
    }

    .traffic-strategy-choice = { $selected ->
    [1] 🔘 { traffic-strategy }
    *[0] ⚪ { traffic-strategy }
    }

    
btn-remnawave =
    .users = <tg-emoji emoji-id="6032609071373226027">👥</tg-emoji> Users
    .hosts = <tg-emoji emoji-id="5776233299424843260">🌐</tg-emoji> Hosts
    .nodes = <tg-emoji emoji-id="5942734685976138521">🖥️</tg-emoji> Nodes
    .inbounds = 🔌 Inbounds

btn-importer =
    .from-xui = 💩 Import from 3X-UI panel
    .sync-from-panel = <tg-emoji emoji-id="5769248574499983619">🌀</tg-emoji> Sync: panel → bot
    .sync-from-bot = <tg-emoji emoji-id="6030400221232501136">🤖</tg-emoji> Sync: bot → panel
    .sync-start = <tg-emoji emoji-id="5773626993010546707">▶️</tg-emoji> Synchronize
    .squads = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Internal squads
    .import-all = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Import all
    .import-active = ❇️ Import active

btn-subscription =
    .plan = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Proceed to subscription
    .new = <tg-emoji emoji-id="5904462880941545555">💸</tg-emoji> Buy subscription
    .renew = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Renew
    .change = <tg-emoji emoji-id="6039779802741739617">🔃</tg-emoji> Change
    .promocode = <tg-emoji emoji-id="5890727932011223292">🎟</tg-emoji> Activate promocode
    .promocode-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Confirm
    .pay = <tg-emoji emoji-id="5805331990618053402">💳</tg-emoji> Pay
    .get = <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji> Get for free
    .back-plans = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Back to plan selection
    .back-duration = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Change duration
    .back-payment-method = <tg-emoji emoji-id="5960671702059848143">⬅️</tg-emoji> Change payment method
    .connect = <tg-emoji emoji-id="5776078972659962594">🚀</tg-emoji> Connect

    .payment-method = { $gateway_title } | { $final_amount ->
    [0] <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji>
    *[HAS] { $final_amount }{ $currency }
    }
    
    .duration = { $period } | { $final_amount -> 
    [0] <tg-emoji emoji-id="6032644646587338669">🎁</tg-emoji>
    *[HAS] { $final_amount }{ $currency }
    }

btn-ad-links =
    .save = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Save
    .create = <tg-emoji emoji-id="5895669571058142797">🆕</tg-emoji> Create link
    .create-confirm = <tg-emoji emoji-id="5774022692642492953">✅</tg-emoji> Create link
    .delete = <tg-emoji emoji-id="5774077015388852135">❌</tg-emoji> Delete link
    .name = <tg-emoji emoji-id="5886285355279193209">🏷️</tg-emoji> Name
    .code = <tg-emoji emoji-id="6028171274939797252">🔗</tg-emoji> Code
    .regenerate = <tg-emoji emoji-id="6030657343744644592">🔄</tg-emoji> Regenerate
    .stats = <tg-emoji emoji-id="5936143551854285132">📊</tg-emoji> Statistics
    .url = <tg-emoji emoji-id="6034969813032374911">📋</tg-emoji> Copy link

    .title = { $is_active ->
    [1] 🟢
    *[0] 🔴
    } { $name }

    .active-toggle = { $is_active ->
    [1] 🟢 Enabled
    *[0] 🔴 Disabled
    }
