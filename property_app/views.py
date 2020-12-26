from django.shortcuts import render, redirect
from property_app.models import ENV, APPLICATION, DOMAIN, LANUAGE, IDC
from django.core.paginator import Paginator


def cmdb_admin(request):
    ret_lanuage = LANUAGE.objects.all().order_by('id')
    return render(request, 'admin.html', {'ret_lanuage': ret_lanuage})


def language_add(request):
    if request.method == 'POST':
        lanuage = request.POST.get('lanuage')
        LANUAGE.objects.create(lanuage=lanuage)
        return redirect('/property/language/')
    return render(request, 'language_add.html')


def language_del(request):
    del_id = request.GET.get('id')
    LANUAGE.objects.filter(id=del_id).delete()
    ENV.objects.filter(lanuage_id=del_id)
    ret = LANUAGE.objects.all()
    return render(request, 'admin.html', {'ret': ret})


def env(request):
    env_id = request.GET.get('lanuage_id')
    try:
        lanuage_id = ENV.objects.filter(lanuage_id=env_id)[0].lanuage_id
    except IndexError:
        lanuage_id = env_id
    except BaseException:
        lanuage_id = ENV.objects.get(id=env_id).lanuage_id
    env_ret = ENV.objects.filter(lanuage_id=lanuage_id)
    return render(request, 'env.html', {'env_ret': env_ret, 'lanuage_id': lanuage_id})


def env_list(request):
    lanuage_id = request.GET.get('id')
    env_ret = ENV.objects.filter(lanuage_id=lanuage_id)
    hostList = []
    for e in env_ret:
        obj = APPLICATION.objects.filter(env_id=e.id)
        for a in obj:
            appList = []
            domainList = []
            ipList = []
            application = a.application
            application_id = a.id
            appList.append(application)
            obj_doamin = DOMAIN.objects.filter(application_id=application_id)
            obj_idc = APPLICATION.objects.get(id=application_id).idc.all()
            for d in obj_doamin:
                domain = d.domain
                domainList.append(domain)
            for i in obj_idc:
                ip = i.ip
                ipList.append(ip)
            appList.append(domainList)
            appList.append(ipList)
            hostList.append(appList)
    paginator = Paginator(hostList, 10)
    page_num = request.GET.get('page', 1)
    page_of_host = paginator.get_page(page_num)
    context = {}
    context['page_of_host'] = page_of_host
    context['hostList'] = page_of_host.object_list
    context['env_ret'] = env_ret
    context['lanuage_id'] =lanuage_id
    return render(request, 'env_list.html', context)


def env_add(request):
    lanuage_id = request.GET.get('lanuage_id')
    if request.method == 'POST':
        env = request.POST.get('env')
        ENV.objects.create(env=env, lanuage_id=lanuage_id)
        return redirect('/property/env/?lanuage_id=%s' % lanuage_id)
    return render(request, 'env_add.html', {'lanuage_id': lanuage_id})


def env_edit(request):
    lanuage_id = request.GET.get('lanuage_id')
    env_id = request.GET.get('env_id')
    if request.method == 'POST':
        env = request.POST.get('env')
        obj = ENV.objects.get(id=env_id)
        obj.env = env
        obj.save()
        return redirect('/property/env/?lanuage_id=%s&env_id=%s' % (lanuage_id, env_id))
    return render(request, 'env_edit.html', {'lanuage_id': lanuage_id, 'env_id': env_id})


def env_del(request):
    del_id = request.GET.get('env_id')
    lanuage_id = ENV.objects.get(id=del_id).lanuage_id
    ENV.objects.filter(id=del_id).delete()
    return redirect('/property/env/?lanuage_id=%s' % lanuage_id)


def app(request):
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    try:
        env_id = APPLICATION.objects.filter(env_id=env_id)[0].env_id
    except IndexError:
        env_id = env_id
    except BaseException:
        env_id = APPLICATION.objects.get(id=env_id).env_id
    ret_app = APPLICATION.objects.filter(env_id=env_id)
    return render(request, 'app.html', {'ret_app': ret_app, 'env_id': env_id, 'lanuage_id': lanuage_id})


def app_add(request):
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    if request.method == 'POST':
        print('app_add_lanuage_id:%s' % lanuage_id)
        app = request.POST.get('app')
        APPLICATION.objects.create(application=app, env_id=env_id)
        return redirect('/property/app/?env_id=%s&lanuage_id=%s' % (env_id, lanuage_id))
    return render(request, 'app_add.html', {'env_id': env_id, 'lanuage_id': lanuage_id})


def app_idc_add(request):
    idc_id = request.GET.get('idc_id')
    if request.method == 'POST':
        app = request.POST.get('app')
        app_id = APPLICATION.objects.get(application=app).id
        obj = IDC.objects.get(id=idc_id)
        obj.APPLICATION.add(app_id)
        return redirect('/property/app_idc_list/?idc_id=%s' % idc_id)
    return render(request, 'app_idc_add.html', {'idc_id': idc_id})


def app_idc_list(request):
    idc_id = request.GET.get('idc_id')
    obj = IDC.objects.get(id=idc_id)
    ret = obj.APPLICATION.all()
    paginator = Paginator(ret, 10)
    page_num = request.GET.get('page', 1)
    page_of_host = paginator.get_page(page_num)
    context = {}
    context['page_of_host'] = page_of_host
    context['ret'] = page_of_host.object_list
    context['idc_id'] = idc_id
    return render(request, 'app_idc_list.html', context)


def app_idc_del(request):
    del_id = request.GET.get('application_id')
    idc_id = request.GET.get('idc_id')
    obj = IDC.objects.get(id=idc_id)
    obj.APPLICATION.remove(del_id)
    return redirect('/property/app_idc_list/?idc_id=%s' % idc_id)


def app_edit(request):
    lanuage_id = request.GET.get('lanuage_id')
    env_id = request.GET.get('env_id')
    application_id = request.GET.get('application_id')
    if request.method == 'POST':
        app = request.POST.get('app')
        obj = APPLICATION.objects.get(id=application_id)
        obj.application = app
        obj.save()
        return redirect('/property/app/?lanuage_id=%s&env_id=%s' % (lanuage_id, env_id))
    return render(request, 'app_edit.html', {'lanuage_id': lanuage_id, 'env_id': env_id, 'application_id': application_id})


def app_del(request):
    del_id = request.GET.get('application_id')
    lanuage_id = request.GET.get('lanuage_id')
    env_id = APPLICATION.objects.get(id=del_id).env_id
    APPLICATION.objects.filter(id=del_id).delete()
    return redirect('/property/app/?env_id=%s&lanuage_id=%s' % (env_id, lanuage_id))


def domain(request):
    application_id = request.GET.get('application_id')
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    try:
        application_id = DOMAIN.objects.filter(application=application_id)[0].application_id
    except IndexError:
        application_id = application_id
    except BaseException:
        application_id = DOMAIN.objects.get(id=application_id).application_id
    ret_domain = DOMAIN.objects.filter(application_id=application_id)
    return render(request, 'domain.html', {'ret_domain': ret_domain, 'application_id': application_id, 'env_id': env_id, 'lanuage_id': lanuage_id})


def domain_add(request):
    application_id = request.GET.get('application_id')
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    if request.method == 'POST':
        domain = request.POST.get('domain')
        DOMAIN.objects.create(domain=domain, application_id=application_id)
        return redirect('/property/domain/?application_id=%s&env_id=%s&lanuage_id=%s' % (application_id, env_id, lanuage_id))
    return render(request, 'domain_add.html', {'application_id': application_id, 'env_id': env_id, 'lanuage_id': lanuage_id})


def domain_edit(request):
    lanuage_id = request.GET.get('lanuage_id')
    env_id = request.GET.get('env_id')
    application_id = request.GET.get('application_id')
    domain_id = request.GET.get('domain_id')
    if request.method == 'POST':
        domain = request.POST.get('domain')
        obj = DOMAIN.objects.get(id=domain_id)
        obj.domain = domain
        obj.save()
        return redirect('/property/domain/?lanuage_id=%s&env_id=%s&application_id=%s' % (lanuage_id, env_id, application_id))
    return render(request, 'domain_edit.html', {'lanuage_id': lanuage_id, 'env_id': env_id, 'application_id': application_id, 'domain_id': domain_id})


def domain_del(request):
    del_id = request.GET.get('domain_id')
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    application_id = DOMAIN.objects.get(id=del_id).application_id
    DOMAIN.objects.filter(id=del_id).delete()
    return redirect('/property/domain/?application_id=%s&env_id=%s&lanuage_id=%s' % (application_id, env_id, lanuage_id))


def idc(request):
    application_id = request.GET.get('application_id')
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    obj = APPLICATION.objects.get(id=application_id)
    ret_idc = obj.idc.all()
    return render(request, 'idc.html', {'ret_idc': ret_idc, 'application_id': application_id, 'env_id': env_id, 'lanuage_id': lanuage_id})


def idc_add(request):
    application_id = request.GET.get('application_id')
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    if request.method == 'POST':
        ip = request.POST.get('ip')
        idc_id = IDC.objects.get(ip=ip).id
        print(idc_id)
        obj = APPLICATION.objects.get(id=application_id)
        obj.idc.add(idc_id)
        return redirect('/property/idc/?application_id=%s&env_id=%s&lanuage_id=%s' % (application_id, env_id, lanuage_id))
    return render(request, 'idc_add.html', {'application_id': application_id, 'env_id': env_id, 'lanuage_id': lanuage_id})


def idc_edit(request):
    idc_id = request.GET.get('idc_id')
    field = request.GET.get('field')
    if request.method == 'POST':
        obj = IDC.objects.get(id=idc_id)
        if field == 'vendors':
            vendors = request.POST.get('vendors')
            obj.vendors = vendors
        elif field == 'system':
            system = request.POST.get('system')
            obj.system = system
        elif field == 'region':
            region = request.POST.get('region')
            obj.region =region
        elif field == 'ip':
            ip = request.POST.get('ip')
            obj.ip = ip
        elif field == 'status':
            status = request.POST.get('status')
            obj.status = status
        elif field == 'configuration':
            configuration = request.POST.get('configuration')
            obj.configuration = configuration
        elif field == 'edit':
            vendors = request.POST.get('vendors')
            obj.vendors = vendors
            system = request.POST.get('system')
            obj.system = system
            region = request.POST.get('region')
            obj.region =region
            ip = request.POST.get('ip')
            obj.ip = ip
            status = request.POST.get('status')
            obj.status = status
            configuration = request.POST.get('configuration')
            obj.configuration = configuration
        obj.save()
        return redirect('/property/idc_all/')
    return render(request, 'idc_edit.html', {'idc_id': idc_id, 'field': field})


def idc_del(request):
    del_id = request.GET.get('idc_id')
    env_id = request.GET.get('env_id')
    lanuage_id = request.GET.get('lanuage_id')
    application_id = request.GET.get('application_id')
    obj = APPLICATION.objects.get(id=application_id)
    obj.idc.remove(del_id)
    return redirect('/property/idc/?application_id=%s&env_id=%s&lanuage_id=%s' % (application_id, env_id, lanuage_id))


def idc_all(request):
    ret_idc_all = IDC.objects.all()
    paginator = Paginator(ret_idc_all, 10)
    page_num = request.GET.get('page', 1)
    page_of_host = paginator.get_page(page_num)
    context = {}
    context['page_of_host'] = page_of_host
    context['ret_idc_all'] = page_of_host.object_list
    return render(request, 'idc_all.html', context)


def idc_all_add(request):
    if request.method == 'POST':
        vendors = request.POST.get('vendors')
        system = request.POST.get('system')
        region = request.POST.get('region')
        ip = request.POST.get('ip')
        status = request.POST.get('status')
        configuration = request.POST.get('configuration')
        IDC.objects.create(vendors=vendors, system=system, region=region, ip=ip, status=status, configuration=configuration)
        return redirect('/property/idc_all/')
    return render(request, 'idc_all_add.html')


def idc_all_del(request):
    del_id = request.GET.get('idc_id')
    IDC.objects.filter(id=del_id).delete()
    return redirect('/property/idc_all/')


def host_list(request):
    env_id = request.GET.get('env_id')
    env = ENV.objects.get(id=env_id).env
    lanuage_id = request.GET.get('lanuage_id')
    obj = APPLICATION.objects.filter(env_id=env_id)
    hostList = []
    for a in obj:
        appList = []
        domainList = []
        ipList = []
        application = a.application
        application_id = a.id
        appList.append(application)
        obj_doamin = DOMAIN.objects.filter(application_id=application_id)
        obj_idc = APPLICATION.objects.get(id=application_id).idc.all()
        for d in obj_doamin:
            domain = d.domain
            domainList.append(domain)
        for i in obj_idc:
            ip = i.ip
            ipList.append(ip)
        appList.append(domainList)
        appList.append(ipList)
        hostList.append(appList)
    paginator = Paginator(hostList, 10)
    page_num = request.GET.get('page', 1)
    page_of_host = paginator.get_page(page_num)
    context = {}
    context['page_of_host'] = page_of_host
    context['hostList'] = page_of_host.object_list
    context['lanuage_id'] = lanuage_id
    context['env'] = env
    context['env_id'] = env_id
    return render(request, 'host_list.html', context)


def home(request):
    obj = APPLICATION.objects.all()
    hostList = []
    for a in obj:
        appList = []
        domainList = []
        ipList = []
        application = a.application
        application_id = a.id
        appList.append(application)
        obj_doamin = DOMAIN.objects.filter(application_id=application_id)
        obj_idc = APPLICATION.objects.get(id=application_id).idc.all()
        for d in obj_doamin:
            domain = d.domain
            domainList.append(domain)
        for i in obj_idc:
            ip = i.ip
            ipList.append(ip)
        appList.append(domainList)
        appList.append(ipList)
        hostList.append(appList)
    paginator = Paginator(hostList, 10)
    page_num = request.GET.get('page', 1)
    page_of_host = paginator.get_page(page_num)
    context = {}
    context['page_of_host'] = page_of_host
    context['hostList'] = page_of_host.object_list
    return render(request, 'home.html', context)


