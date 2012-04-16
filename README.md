# Django urls introspect


Introspect django urlpatterns to find potential bugs. Comes in handy during refactoring projects or as an extra sanity check

[ blog post ](http://www.szotten.com/david/introspecting-django-urls-for-fun-and-profit.html)

## Usage

    ./manage check_urs
    edit-members: url provides kwargs ['member_id'] not in the view sinature
    edit-members: view requires kwargs ['member_code'] not in the url kwargs


## License
MIT License
