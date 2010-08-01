
class Permission(object):
    """
    Class which holds routines to check if user has permissions for 
    a specific action.
    """
    
    @staticmethod
    def user_is_author(user):
        """
        Determine if user can access and create drafts.
        """
        return user.is_staff
    
    @staticmethod
    def user_is_editor(user):
        """
        Determine if user can modify other authors' document.
        """
        return user.is_superuser
    
    @staticmethod
    def user_is_reader(user):
        """
        Determine if user can read publised documents.
        """
        return True
        
    @staticmethod
    def user_is_reviewer(user):
        """
        Determine if user can post comments on published documents.
        """
        return user.is_authenticated