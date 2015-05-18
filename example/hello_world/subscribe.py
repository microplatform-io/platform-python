import microplatform

service = microplatform.get_default_service('documentation-list-get')

@service.handle(microplatform.GET, microplatform.DOCUMENTATION_LIST)
def get_documentation(request):
    documentation_list = microplatform.DocumentationList().FromString(request.body)

    print "DOCUMENTATION LIST: %s" % (documentation_list, )

    return microplatform.RoutedMessage(
        method      = microplatform.REPLY, 
        resource    = microplatform.DOCUMENTATION_LIST, 
        body        = documentation_list.SerializeToString()
    )

service.run()