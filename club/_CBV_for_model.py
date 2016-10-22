class PlayerCreate(CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'club/player_form.html'
   #field = []


class PlayerCreateCustom(CreateView):
    model = Person
    # Do not specify fieds together with form class! It will throw exception
    # fields = ['sname']
    form_class = PersonForm
    template_name = 'club/player_create.html'


    # Not typical use to overwrite
    #def get_form(self,**kwargs):
    #    print("At get_form")

    def form_invalid(self,form):
        print("At form_invalid")
        print(form)
        print(form.cleaned_data)
        return HttpResponseRedirect('/club/')

    def form_valid(self,form):
        print("At form_valid")

        # self.request_user is not valid not avail, do not try as per example
        #print("Request User: %s" % (self.request_user))
        #return HttpResponseRedirect('/club/')

        
        #form.instance.person_type = form.cleaned_data['person_type']
        return super(PlayerCreateCustom,self).form_valid(form)

class PlayerDetail(DetailView):
    model = Person
    template_name = 'club/player_detail.html'

class PlayerList(ListView):
    model = Person
    template_name = 'club/player_list.html'

class PlayerUpdate(UpdateView):
    model = Person    
    form_class = PersonForm
    template_name = 'club/player_form.html'
    success_url = reverse_lazy('player_list')

class PlayerDelete(DeleteView):
    model = Person    
    template_name = 'club/player_confirm_delete.html'
    success_url = reverse_lazy('player_list')