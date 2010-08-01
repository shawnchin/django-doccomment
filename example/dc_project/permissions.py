
class Permission(object):
    """
    Custom permission class to allow all registered users to create
    documents and post comments.
    
    Only staff can modify other users' document.
    """
    
    @staticmethod
    def user_can_view_draft(user):
        """
        Determine if user can view drafts
        """
        return True
        
    @staticmethod
    def user_can_create_draft(user):
        """
        Determine if user can create drafts.
        
        This should at the very least restrict anonymous users else we can't 
        assign the draft to an author.
        """
        return user.is_authenticated()
    
    @staticmethod
    def user_is_editor(user):
        """
        Determine if user can modify other authors' document.
        """
        return user.is_staff
    
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