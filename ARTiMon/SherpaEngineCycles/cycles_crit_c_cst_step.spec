* // signaux
cycleid
distance
elecpower
socelec
fuelpower
socfuel
speed
* // sous_formules
false = ('bool_cst' 0)

cycle_start = Top0 cycleid

in_cycle = ! cycle_start

cycle_end = Bot cycleid

cycle_stable = !  cycle_end





//---------- pour crit_c -----------

// conversion en entier 0/1 de la proposition bool�enne "elecpower < 0"
	pe_negative_array[2] elecpower ('double_cst' 0)
	pe_negative_int = # ('<' pe_negative_array)

// restriction de la puissance aux instants o� elle n�gative 
	pe_negative_or_null_[2] pe_negative_int elecpower
	pe_negative_or_null =  '*' pe_negative_or_null_
	
//	coupure par cycle et compl�tion � null des instants non d�finis
	pe_negative_or_null_by_cycle = # (cycle_stable & pe_negative_or_null)


// int�grale par cycle
	integrale_pe_by_cycle =  cycle_end & (A{'sum'}[<,0] pe_negative_or_null_by_cycle)
	
// int�grale au moment de la fin de cycle

  
integ_sur_cbat_vec[2] integrale_pe_by_cycle ('double_cst' 160218000)


*

crit_c =  ('div' integ_sur_cbat_vec) & false