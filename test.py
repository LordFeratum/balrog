from balrog import Balrog, IdentityContext

balrog = Balrog()

balrog.add_role("member")
balrog.add_role("student", ["member"])
balrog.add_role("teacher", ["member"])

balrog.add_resource("course")

balrog.allow("member", "view", "course")
balrog.allow("student", "learn", "course")
balrog.allow("teacher", "teach", "course")

context = IdentityContext(balrog)


@context.role_loader
def role_loader():
    return ["member", "student"]


@context.role_loader
def role_loader_two():
    return ["teacher"]


@context.check("jamon", "course", message="Error on 'yes'")
def yes():
    print("YES!")


yes()
