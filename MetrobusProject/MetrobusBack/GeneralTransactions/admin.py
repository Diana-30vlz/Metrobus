from django.contrib import admin
from .models import Merchant, BankAccount, Seller, Terminal, GmrFile, Transaction


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'name')
    search_fields = ('rfc', 'name')


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('num_account', 'currency_code')
    search_fields = ('num_account',)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('cod_seller', 'name', 'merchant', 'bank_account', 'line', 'terminal_type', 'payment_scheme')
    list_filter = ('merchant', 'terminal_type', 'payment_scheme')
    search_fields = ('cod_seller', 'name')


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('id_terminal', 'seller')
    list_filter = ('seller__merchant',)
    search_fields = ('id_terminal', 'seller__name', 'seller__cod_seller')


@admin.register(GmrFile)
class GmrFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'merchant', 'download_date', 'total_rows', 'status')
    list_filter = ('status', 'merchant')
    search_fields = ('filename',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id_transaction', 'seller', 'dat_transaction',
        'amt_gross', 'amt_net', 'tx_status', 'card_brand',
    )
    list_filter = ('tx_status', 'card_brand', 'dat_settlement')
    search_fields = ('id_transaction', 'cod_authorization', 'num_card')
    date_hierarchy = 'dat_transaction'
    raw_id_fields = ('file', 'seller', 'terminal')
