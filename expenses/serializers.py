def serialize_payers(payers_queryset):
    return [
        {
            'user_id': payer.user.id,
            'username': payer.user.username,
            'paid_amount': str(payer.paid_amount),
        }
        for payer in payers_queryset
    ]


def serialize_shares(shares_queryset):
    return [
        {
            'user_id': share.user.id,
            'username': share.user.username,
            'share_amount': str(share.share_amount),
        }
        for share in shares_queryset
    ]
