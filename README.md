# Project_site_django


models includes(user ,product , profile, category, order, itemorder)
 product -> foreignkey (category)
 order -> foreignkey (user)
 itemorder -> foreignkey (order, product)
 profile -> foreignkey (user)
 
user can signup or login..
user can order the product or delete own order..
the cost of the orders is specified in property model..
Authentication is done with token..
just admin can create product and category (Handled in permissions)..
if user not Authenticated just see list product..
