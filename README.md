# What the heck is a "Balrog"?

According to [Wikipedia](https://en.wikipedia.org/wiki/Balrog): Balrogs /ˈbælrɒɡz/ are fictional creatures who appear in J. R. R. Tolkien's Middle-earth legendarium. 


# What this project is called "Balrog"?

In Moria, when Gandalf confronts the Balrog on the bridge of Khazad-dûm, Gandalf says the following:

> I am a servant of the Secret Fire, wielder of the flame of Anor. You cannot pass! The dark fire will not avail you, flame of Udûn. Go back to the Shadow! You cannot pass!

So, Gandalf manage to stop the Balrog to pass through the bridge because he does not have the right role (balrog), instead, the Hobbits and the others can pass, because they have the rigth roles (fellowship).


# How it works?

    from app import get_current_user
    from balrog import Balrog, IdentityContext

    balrog = Balrog()
    context = IdentityContext(balrog)

    balrog.add_role("member")
    balrog.add_role("developer", ["member"])
    balrog.add_role("project-owner", ["member"])

    balrog.add_resource("jira-ticket")

    balrog.allow("member", "view", "jira-ticket")
    balrog.allow("developer", "change-status", "jira-ticket")
    balrog.deny("developer", "create", "jira-ticket")
    balrog.allow("project-owner", "create", "jira-ticket")

    balrog.is_allowed("developer", "view", "jira-ticket")  # True
    balrog.is_allowed("developer", "create", "jira-ticket")  # False
    balrog.is_allowed("project-owner", "view", "jira-ticket")  # True
    balrog.is_allowed("project-owner", "create", "jira-ticket")  # True
    balrog.is_allowed("project-owner", "change-status", "jira-ticket")  # None, it has been defined


    @context.role_loader
    def role_loader():
        yield "everybody"
	user = get_current_user()
	for role in user.get_roles():
	    yield role


    @context.check("view", "jira-ticket")
    def protected():
        print("This method is checked for all the roles that the loader gives, and raises an exepction if noone matches.")    
