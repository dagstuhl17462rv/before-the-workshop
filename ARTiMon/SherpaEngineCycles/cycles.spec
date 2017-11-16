* // signaux
cycle_id
distance
puissance_elec
sOC_Elec
puissance_Fuel
sOC_Fuel
speed
* // sous_formules
false = ('bool_cst' 0)

cycle_start = Top0 cycle_id

in_cycle = ! cycle_start

cycle_end = Bot cycle_id

cycle_stable = ! (E[-0.0625,0] cycle_end)

just_before_cycle_end = V[0.0625 ] cycle_end



//---------- pour crit_c -----------

// conversion en entier 0/1 de la proposition bool�enne "puissance_elec < 0"
	pe_negative_array[2] puissance_elec ('double_cst' 0)
	pe_negative_int = # ('<' pe_negative_array)

// restriction de la puissance aux instants o� elle n�gative 
	pe_negative_or_null_[2] pe_negative_int puissance_elec
	pe_negative_or_null =  '*' pe_negative_or_null_
	
//	coupure par cycle et compl�tion � DOUBLE_MAX des instants non d�finis
//  # applied to a boolean function transforms false into (double) 0 and true into (double) 1
//  # applied to a non boolean transforms nil into DOUBLE_MAX and is identity either
//  DOUBLE_MAX resets the 'sum'  aggregation i.e. sum(DOUBLE_MAX,A) = 0 for any aggregate A

	pe_negative_or_null_by_cycle = # (cycle_stable & pe_negative_or_null)

//	surfaces �l�mentaires 
	li_pe_neg = (LI pe_negative_or_null_by_cycle)
	pe_neg_surface = '*' li_pe_neg

// int�grale par cycle
	integrale_pe_by_cycle =  (A{'sum'}[<=,0] pe_neg_surface)
	
// int�grale au moment de la fin de cycle

	integrale_pe_by_cycle_at_end =  (just_before_cycle_end & integrale_pe_by_cycle)
	
integ_sur_cbat_vec[2] integrale_pe_by_cycle_at_end ('double_cst' 16021800)


*

crit_c =  ('div' integ_sur_cbat_vec) & false