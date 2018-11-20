from modeltranslation.translator import register, TranslationOptions
from .models import MahilaPratinidhiForm, CommonShavaFields

@register(MahilaPratinidhiForm)
class MahilaPratinidhiFormTranslationOptions(TranslationOptions):
    fields = ('name', 'age', 'marital_status', 'updated_marital_status', 'educational_qualification', 
    'updated_educational_qualification', 'caste', 'updated_caste', 'address', 'contact_number',
    'email', 'nirwachit_padh', 'nirwachit_vdc_or_municipality_name', 'party_name', 'party_joined_date',
    'samlagna_sang_sastha_samuha', 'nirwachit_chetra_pratiko_pratibadhata', )


@register(CommonShavaFields)
class CommonShavaFieldsTranslationOptions(TranslationOptions):
    fields = ('date_of_birth', 'mothers_name', 'fathers_name', 'marital_status', 'updated_marital_status',
    'husbands_name', 'caste', 'updated_caste', 'mother_tongue', 'updated_mother_tongue', 'educational_qualification',
    'updated_educational_qualification', 'subject', 'permanent_address', 'permanent_gapa_napa', 'permanent_ward_no',
    'permanent_tole', 'temporary_address', 'temporary_gapa_napa', 'temporary_ward_no', 'temporary_tole', 
    'mobile', 'contact_number', 'email', 'social_networking_medium', 'nirwachit_prakriya', 'updated_nirwachit_prakriya',
    'nirwachit_padh', 'updated_nirwachit_padh', 'pichidiyeko_chhetra_ho_hoina', 'updated_pichidiyeko_chhetra_ho_hoina',
    'nirwachit_chhetrako_bibaran', 'nirwachit_vayeko_chhetra_aafno_thegana', 'updated_nirwachit_vayeko_chhetra_aafno_thegana',
    'party_name', 'party_joined_date', 'pramukh_jimmewari', 'nirwachit_chetra_pratiko_pratibadhata', 
    'aaja_vanda_agadi_chunab_ladnu_vayeko_chha', 'updated_aaja_vanda_agadi_chunab_ladnu_vayeko_chha',
    'prapta_maat_sankhya', 'samlagna_sang_sastha_samuha', )

