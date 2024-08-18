import re

def validate_date(in_date, out_date):
    date_pattern = r'^(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/\d{4}$'
    
    if not re.match(date_pattern, in_date):
        print(f"Invalid input date format. Expected format: MM/DD/YYYY, but got {in_date}")
        return False
    
    if not re.match(date_pattern, out_date):
        print(f"Invalid output date format. Expected format: MM/DD/YYYY, but got {out_date}")
        return False
    
    return True

def validate_guests(guests):
    if guests < 1:
        return False
    return True


#[<div class="p58w9eu atm_9s_1bgihbq dir dir-ltr"><div class="c1i3jwjb atm_gz_t94yts atm_h0_t94yts c1buxrsh atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_ar_1bp4okc atm_5j_1osqo2v atm_mk_h2mmj6 d1qdcyln b1dbvlpf atm_3f_nneixv atm_7l_1n8btb2 atm_k4_bxt1mx atm_cs_10d11i2 atm_rd_glywfm dir dir-ltr notranslate" data-is-day-blocked="true" data-testid="06/01/2024" style="width: 46px; height: 46px;">1</div></div>]