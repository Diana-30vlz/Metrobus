import uuid
from django.db import models


class Merchant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfc = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'merchants'

    def __str__(self):
        return f"{self.rfc} - {self.name}"


class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_account = models.CharField(max_length=30, unique=True)
    currency_code = models.SmallIntegerField(default=484)

    class Meta:
        db_table = 'bank_accounts'

    def __str__(self):
        return self.num_account


class Seller(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT, related_name='sellers')
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, related_name='sellers')
    cod_seller = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    line = models.CharField(max_length=50, blank=True, null=True)
    terminal_type = models.CharField(max_length=20, blank=True, null=True)
    payment_scheme = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'sellers'

    def __str__(self):
        return f"{self.cod_seller} - {self.name}"


class Terminal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, related_name='terminals')
    id_terminal = models.CharField(max_length=50, db_index=True)

    class Meta:
        db_table = 'terminals'
        unique_together = ('seller', 'id_terminal')

    def __str__(self):
        return f"{self.id_terminal} ({self.seller.name})"


class GmrFile(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PROCESSED = 'processed'
    STATUS_ERROR = 'error'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_PROCESSED, 'Processed'),
        (STATUS_ERROR, 'Error'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT, related_name='gmr_files')
    filename = models.CharField(max_length=200, unique=True)
    download_date = models.DateTimeField()
    total_rows = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

    class Meta:
        db_table = 'gmr_files'

    def __str__(self):
        return self.filename


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(GmrFile, on_delete=models.PROTECT, related_name='transactions')
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, related_name='transactions')
    terminal = models.ForeignKey(
        Terminal, on_delete=models.PROTECT, related_name='transactions',
        null=True, blank=True
    )

    # Identificadores Getnet
    id_transaction = models.CharField(max_length=100, unique=True)
    id_settlement = models.CharField(max_length=100, blank=True, null=True)
    id_external_order = models.CharField(max_length=100, blank=True, null=True)
    id_external_payment = models.CharField(max_length=100, blank=True, null=True)
    cod_authorization = models.CharField(max_length=50, blank=True, null=True)
    cod_arn = models.CharField(max_length=100, blank=True, null=True)
    cod_rrn = models.CharField(max_length=50, blank=True, null=True)
    cod_stan = models.BigIntegerField(null=True, blank=True)

    # Tipo y estado
    des_mov_type = models.CharField(max_length=50, blank=True, null=True)
    des_identity_origin_type = models.CharField(max_length=100, blank=True, null=True)
    nam_identity_origin = models.CharField(max_length=200, blank=True, null=True)
    tx_type = models.CharField(max_length=50, blank=True, null=True)
    tx_status = models.CharField(max_length=50, blank=True, null=True)
    tx_channel = models.CharField(max_length=50, blank=True, null=True)
    op_type = models.CharField(max_length=50, blank=True, null=True)
    des_authorizer_switch = models.CharField(max_length=100, blank=True, null=True)
    des_settlement_type = models.CharField(max_length=100, blank=True, null=True)
    des_settlement_status = models.CharField(max_length=50, blank=True, null=True)

    # Fechas y hora
    dat_transaction = models.DateField(null=True, blank=True)
    tim_transaction = models.TimeField(null=True, blank=True)
    num_timezone = models.SmallIntegerField(null=True, blank=True)
    dat_settlement = models.DateField(null=True, blank=True)
    dat_settled = models.DateField(null=True, blank=True)
    dat_original_transaction = models.DateField(null=True, blank=True)

    # Tarjeta
    des_card_entry_mode = models.CharField(max_length=50, blank=True, null=True)
    num_card = models.CharField(max_length=30, blank=True, null=True)
    card_funding = models.CharField(max_length=30, blank=True, null=True)
    card_brand = models.CharField(max_length=50, blank=True, null=True)
    card_issuer = models.CharField(max_length=200, blank=True, null=True)
    card_interchange = models.CharField(max_length=100, blank=True, null=True)
    card_country = models.CharField(max_length=5, blank=True, null=True)
    card_product = models.CharField(max_length=100, blank=True, null=True)
    des_authentication_method = models.CharField(max_length=100, blank=True, null=True)

    # Montos principales
    amt_gross = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amt_net = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    cod_currency = models.SmallIntegerField(null=True, blank=True)
    amt_net_currency = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amt_total_fee = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amt_total_vat = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amt_original_transaction = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    id_original_transaction = models.CharField(max_length=100, blank=True, null=True)

    # MDR
    mdr_type = models.CharField(max_length=50, blank=True, null=True)
    amt_mdr = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    pct_mdr = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    pct_mdr_transaction_fee = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    amt_mdr_vat = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    pct_mdr_vat = models.CharField(max_length=20, blank=True, null=True)

    # Costos de red
    amt_interchange = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    pct_interchange = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    amt_scheme_cost = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    pct_scheme_cost = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    amt_markup = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    pct_markup = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    amt_fix_cost = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)

    # Meses sin intereses
    flag_installment = models.BooleanField(null=True, blank=True)
    des_installment_plan_type = models.CharField(max_length=100, blank=True, null=True)
    des_installment_schema = models.CharField(max_length=100, blank=True, null=True)
    num_total_installments = models.SmallIntegerField(null=True, blank=True)
    num_installment = models.SmallIntegerField(null=True, blank=True)
    amt_installment = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amt_total_installment_tx = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amt_installment_fee = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)

    # Cashback y DCC
    flag_cashback = models.BooleanField(null=True, blank=True)
    amt_cashback = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    amt_fee_cashback = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)
    flag_dcc = models.BooleanField(null=True, blank=True)
    cod_currency_dcc = models.SmallIntegerField(null=True, blank=True)
    amt_dcc_rebate = models.DecimalField(max_digits=14, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['dat_transaction']),
            models.Index(fields=['dat_settlement']),
            models.Index(fields=['seller']),
            models.Index(fields=['card_brand']),
            models.Index(fields=['tx_status']),
        ]

    def __str__(self):
        return self.id_transaction
