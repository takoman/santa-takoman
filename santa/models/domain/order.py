# -*- coding: utf-8 -*-

from mongoengine import *
from mongoengine import signals
import datetime
from santa.models.mixins.updated_at_mixin import UpdatedAtMixin
from santa.models.domain.user import User

__all__ = ('Order',)

SUPPORTED_CURRENCIES = [
    u'TWD',   # Taiwan New Dollar
    u'AED',   # United Arab Emirates Dirham
    # u'AFN', # Afghanistan Afghani
    # u'ALL', # Albania Lek
    # u'AMD', # Armenia Dram
    # u'ANG', # Netherlands Antilles Guilder
    # u'AOA', # Angola Kwanza
    u'ARS',   # Argentina Peso
    u'AUD',   # Australia Dollar
    # u'AWG', # Aruba Guilder
    # u'AZN', # Azerbaijan New Manat
    # u'BAM', # Bosnia and Herzegovina Convertible Marka
    # u'BBD', # Barbados Dollar
    # u'BDT', # Bangladesh Taka
    # u'BGN', # Bulgaria Lev
    # u'BHD', # Bahrain Dinar
    # u'BIF', # Burundi Franc
    # u'BMD', # Bermuda Dollar
    # u'BND', # Brunei Darussalam Dollar
    # u'BOB', # Bolivia Boliviano
    u'BRL',   # Brazil Real
    # u'BSD', # Bahamas Dollar
    # u'BTN', # Bhutan Ngultrum
    # u'BWP', # Botswana Pula
    # u'BYR', # Belarus Ruble
    # u'BZD', # Belize Dollar
    u'CAD',   # Canada Dollar
    # u'CDF', # Congo/Kinshasa Franc
    u'CHF',   # Switzerland Franc
    # u'CLP', # Chile Peso
    u'CNY',   # China Yuan Renminbi
    u'COP',   # Colombia Peso
    # u'CRC', # Costa Rica Colon
    # u'CUC', # Cuba Convertible Peso
    # u'CUP', # Cuba Peso
    # u'CVE', # Cape Verde Escudo
    # u'CZK', # Czech Republic Koruna
    # u'DJF', # Djibouti Franc
    # u'DKK', # Denmark Krone
    # u'DOP', # Dominican Republic Peso
    # u'DZD', # Algeria Dinar
    # u'EGP', # Egypt Pound
    # u'ERN', # Eritrea Nakfa
    # u'ETB', # Ethiopia Birr
    u'EUR',   # Euro Member Countries
    # u'FJD', # Fiji Dollar
    # u'FKP', # Falkland Islands (Malvinas) Pound
    u'GBP',   # United Kingdom Pound
    # u'GEL', # Georgia Lari
    # u'GGP', # Guernsey Pound
    # u'GHS', # Ghana Cedi
    # u'GIP', # Gibraltar Pound
    # u'GMD', # Gambia Dalasi
    # u'GNF', # Guinea Franc
    # u'GTQ', # Guatemala Quetzal
    # u'GYD', # Guyana Dollar
    u'HKD',   # Hong Kong Dollar
    # u'HNL', # Honduras Lempira
    # u'HRK', # Croatia Kuna
    # u'HTG', # Haiti Gourde
    # u'HUF', # Hungary Forint
    u'IDR',   # Indonesia Rupiah
    u'ILS',   # Israel Shekel
    # u'IMP', # Isle of Man Pound
    u'INR',   # India Rupee
    # u'IQD', # Iraq Dinar
    # u'IRR', # Iran Rial
    u'ISK',   # Iceland Krona
    # u'JEP', # Jersey Pound
    # u'JMD', # Jamaica Dollar
    # u'JOD', # Jordan Dinar
    u'JPY',   # Japan Yen
    # u'KES', # Kenya Shilling
    # u'KGS', # Kyrgyzstan Som
    # u'KHR', # Cambodia Riel
    # u'KMF', # Comoros Franc
    # u'KPW', # Korea (North) Won
    u'KRW',   # Korea (South) Won
    # u'KWD', # Kuwait Dinar
    # u'KYD', # Cayman Islands Dollar
    # u'KZT', # Kazakhstan Tenge
    # u'LAK', # Laos Kip
    # u'LBP', # Lebanon Pound
    # u'LKR', # Sri Lanka Rupee
    # u'LRD', # Liberia Dollar
    # u'LSL', # Lesotho Loti
    # u'LYD', # Libya Dinar
    # u'MAD', # Morocco Dirham
    # u'MDL', # Moldova Leu
    # u'MGA', # Madagascar Ariary
    # u'MKD', # Macedonia Denar
    # u'MMK', # Myanmar (Burma) Kyat
    # u'MNT', # Mongolia Tughrik
    # u'MOP', # Macau Pataca
    # u'MRO', # Mauritania Ouguiya
    # u'MUR', # Mauritius Rupee
    # u'MVR', # Maldives (Maldive Islands) Rufiyaa
    # u'MWK', # Malawi Kwacha
    u'MXN',   # Mexico Peso
    # u'MYR', # Malaysia Ringgit
    # u'MZN', # Mozambique Metical
    # u'NAD', # Namibia Dollar
    # u'NGN', # Nigeria Naira
    # u'NIO', # Nicaragua Cordoba
    # u'NOK', # Norway Krone
    # u'NPR', # Nepal Rupee
    u'NZD',   # New Zealand Dollar
    # u'OMR', # Oman Rial
    # u'PAB', # Panama Balboa
    # u'PEN', # Peru Nuevo Sol
    # u'PGK', # Papua New Guinea Kina
    u'PHP',   # Philippines Peso
    # u'PKR', # Pakistan Rupee
    # u'PLN', # Poland Zloty
    # u'PYG', # Paraguay Guarani
    # u'QAR', # Qatar Riyal
    # u'RON', # Romania New Leu
    # u'RSD', # Serbia Dinar
    u'RUB',   # Russia Ruble
    # u'RWF', # Rwanda Franc
    # u'SAR', # Saudi Arabia Riyal
    # u'SBD', # Solomon Islands Dollar
    # u'SCR', # Seychelles Rupee
    # u'SDG', # Sudan Pound
    # u'SEK', # Sweden Krona
    u'SGD',   # Singapore Dollar
    # u'SHP', # Saint Helena Pound
    # u'SLL', # Sierra Leone Leone
    # u'SOS', # Somalia Shilling
    # u'SPL', # Seborga Luigino
    # u'SRD', # Suriname Dollar
    # u'STD', # São Tomé and Príncipe Dobra
    # u'SVC', # El Salvador Colon
    # u'SYP', # Syria Pound
    u'SZL',   # Swaziland Lilangeni
    # u'THB', # Thailand Baht
    # u'TJS', # Tajikistan Somoni
    # u'TMT', # Turkmenistan Manat
    # u'TND', # Tunisia Dinar
    # u'TOP', # Tonga Pa'anga
    u'TRY',   # Turkey Lira
    # u'TTD', # Trinidad and Tobago Dollar
    # u'TVD', # Tuvalu Dollar
    # u'TZS', # Tanzania Shilling
    # u'UAH', # Ukraine Hryvnia
    # u'UGX', # Uganda Shilling
    # u'USD', # United States Dollar
    # u'UYU', # Uruguay Peso
    # u'UZS', # Uzbekistan Som
    # u'VEF', # Venezuela Bolivar
    u'VND',   # Viet Nam Dong
    # u'VUV', # Vanuatu Vatu
    # u'WST', # Samoa Tala
    # u'XAF', # Communauté Financière Africaine (BEAC) CFA Franc BEAC
    # u'XCD', # East Caribbean Dollar
    # u'XDR', # International Monetary Fund (IMF) Special Drawing Rights
    # u'XOF', # Communauté Financière Africaine (BCEAO) Franc
    # u'XPF', # Comptoirs Français du Pacifique (CFP) Franc
    # u'YER', # Yemen Rial
    u'ZAR',   # South Africa Rand
    # u'ZMW', # Zambia Kwacha
    # u'ZWD', # Zimbabwe Dollar
]

ORDER_STATUSES = [
    u'new', u'invoiced', u'paid', u'merchant_purchased',
    u'merchant_received', u'international_shipped',
    u'domestic_shipped', u'delivered', u'closed',
    u'canceled', u'refunded'
]

class Order(UpdatedAtMixin, Document):
    customer        = ReferenceField(User, required=True)
    merchant        = ReferenceField(User, required=True)  # TODO: Should have a separate Merchant document
    # shipping      = ReferenceField(Shipment)

    status          = StringField(choices=ORDER_STATUSES, default=u'new')
    line_items      = ListField(ReferenceField('OrderLineItem'))
    total           = FloatField()  # in target currency
    currency_source = StringField(choices=SUPPORTED_CURRENCIES)
    currency_target = StringField(choices=SUPPORTED_CURRENCIES, default=u'TWD')

    # All the prices, e.g. order.total and line_item.price, are normalized
    # in target currency. Exchange rate here is for reporting purposes, and
    # updating it won't trigger any price updates. To update prices due to
    # exchange rate update, we have to manually update the line item prices
    # in normalized currency.
    exchange_rate   = FloatField  # source/target, e.g. USD/TWD = 30.00
    notes           = StringField()
    updated_at      = DateTimeField(default=datetime.datetime.now)
    created_at      = DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'orders'
    }

    @classmethod
    def update_total(cls, sender, document, **kwargs):
        order = document
        order.total = order.calculate_total()
        return

    def calculate_total(self):
        return sum([item.price * item.quantity for item in self.line_items])

signals.pre_save_post_validation.connect(Order.update_total, sender=Order)
