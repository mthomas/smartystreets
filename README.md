Unofficial python API for smartystreets.com API.

Usage

l = lookup.Lookup('<auth-id>', '<auth-token>'); 
data = l.lookup(street='123 Main Street', street2='apt 1', city='anytown', state='ny', zip_code='12345', candidates=10)
