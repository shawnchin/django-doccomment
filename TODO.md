TODO
====

* Clean up example code. Isolate doccomment specific JS/CSS/operations and place
  them under the app directory. Use templatetags where possible.
    * Provide minified version of JS/CSS
    * Make example project look more presentable
* Installation docs
* Admin pages
* Test. Test. Test.
* Link to display past versions of published docs
* Print preview of published doc
* template tags to access permissions
* Introduce caching where appropriate
* Implement hide/delete of Documents and Versions
* Use django-reversion for revision history / rollback / diffs
* Generated HTML should use styles from single CSS file (isolate from parent site)
* Generate Table Of Content based on <h?> tags in document
* Use MarkItUp and ShowDown in document editor to allow real-time client-side 
  preview of document (in demo project)
* Reconsider how users can override Permission and Parser modules. Curent method
  feels too much like a hack




GOLD PLATING (or should we leave this app simple?)
==================================================

* Implement CommentStatus
* Allow users to "follow" specific documents (email notification when new 
  versions published)
* Implement Tasks for each document, so authors can set up lists of changes
  to be made.
* Link comment acknolegement with "pending tasks". Workflow:
    1. User adds comments
    2. Author can 'acknowledge' comment to indicate that he/she has read it
        * Comment status changes from 'unread' to 'acknowledged'
    3. Author has option to 'save as task', and give it a title
        * Comment status changes to 'in progress'
        * Author's Task list gets populate with new task
    4. When relevant changes are made in document, author can mark task as
       completed.
        * Comment status changes to 'implemented in draft'
        * Author can still unmark 'completed' comments before draft is 
          published.
    5. When next version published, all tasks completed since last publication
       will be marked as 'publised in version X.Y.Z'
        * Comment status also changes to 'published in version X.Y.Z'
        * Task is archived. It can be browsed, but not modified.
* Allow Authors to add comments when saving document
    * all comments will be published as ChangeLog for next published version
    * Tasks that are completed will also be listed in changelog
    * If task is associated to a comment, a reference to the comment is also
      included.

