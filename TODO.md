TODO
====

* Rip out and clean up code from existing implementation
* Restructure models to improve performance
    * Store Markdown and HTML in Version model
    * Associate Comment to Version (with elem_id) instead of PageElement
    * Use PageElement only for context reference in comment page
* Test. Test. Test.
* Generated HTML should use styles from single CSS file (isolate from parent site)
* Use MarkItUp and ShowDown in document editor to allow real-time client-side 
  preview of document
* Consider allowing HTML in Markdown (if BeautifulSoup can clean up malformed
  tags - prevent document from mucking up parent page layout)
* Allow users to "follow" specific documents (email notification when new 
  versions published)
* Redesign comments - allow multiple backends so we don't override models of
  contrib.comments and break other apps that may also be using Comments.
* Give option for anonymous comments.
* Implement template tags to make it easier for users to integrate 
  doccomment in their own project
* Comments on document view should be imported separetely (JSON via AJAX)
* doccomment specific jquery should be compiled as doccomment.js
* Implement diffs between versions
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

