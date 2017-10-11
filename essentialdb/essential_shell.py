from cmd import Cmd
from essentialdb import EssentialDB

class EssentialPrompt(Cmd):

#    def setup(self):
#        self.db = None


    def do_use(self, args):
        self.db = EssentialDB(filepath=args.strip())
        print(self.db)

    def do_collection(self, args):
        self.collection = self.db.get_collection(args)

    def do_find(self, args):
        print(self.collection.find())

    def do_show(self, args):
        if args == "collections":
            print("Collections:")
            print([c for c in self.db.collections])

    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit


if __name__ == '__main__':
    prompt = EssentialPrompt()

    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')