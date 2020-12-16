from bmes.cataloguebp.models import Brand, Category, StatusType, Product

def fetch_products(request, category_slug, brand_slug):

       page = int(request.args.get('page', 1))
                 
        #Filter the products
       if category_slug == 'all-categories' and  brand_slug == 'all-brands':
            page_object = Product.query.filter_by(product_status = StatusType.Active).paginate(page, 9,  False)

       if category_slug != 'all-categories' and  brand_slug != 'all-brands':
            page_object =  (Product.query.filter_by(product_status =  StatusType.Active)
                              .filter(Product.categories.any(Category.slug ==  category_slug))
                              .filter(Product.brands.any(Brand.slug == brand_slug)).paginate(page, 9,  False)
                             )
       if category_slug != 'all-categories' and  brand_slug == 'all-brands':
            page_object =  (Product.query.filter_by(product_status =  StatusType.Active)
                               .filter(Product.categories.any(Category.slug ==  category_slug)).paginate(page, 9,  False)
                            )
       if category_slug == 'all-categories' and  brand_slug != 'all-brands':
            page_object =  (Product.query.filter_by(product_status =  StatusType.Active)
                              .filter(Product.brands.any(Brand.slug == brand_slug)).paginate(page, 9,  False)
                             )
              
       return page_object

   # The page_object has the following properties and methods:
   # items, pages, prev_num, next_num, iter_pages(), page, has_next, has_prev 