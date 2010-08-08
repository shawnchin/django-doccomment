# TODO: Template tags to access these permissions in template

class Permission(object):
    """
    Class which holds routines to check if user has permissions for 
    a specific action.
    """
    
    @staticmethod
    def user_can_view_draft(user):
        """
        Determine if user can view drafts
        """
        return user.is_staff
        
    @staticmethod
    def user_is_author(user):
        """
        Determine if user can create and publish drafts.
        
        This should at the very least restrict anonymous users else we can't 
        assign the draft to an author.
        """
        return user.is_staff
    
    @staticmethod
    def user_is_editor(user):
        """
        Determine if user can modify other authors' document.
        """
        return user.is_superuser
    
    @staticmethod
    def user_can_view_published(user):
        """
        Determine if user can view publised documents.
        """
        return True
        
    @staticmethod
    def user_can_post_comments(user):
        """
        Determine if user can post comments on published documents.
        """
        return user.is_authenticated