from django.template import Library
from django.utils.html import mark_safe


register = Library()


@register.filter
def comments_filter(comment_list):
    res = """
             <ul class="commentlist">
                {}
             </ul>
             """
    i = ''
    for comment in comment_list:
        i += """
             <li>
                <article class="comment">
                    <section class="comment-details">
                        <div class="author-name">
                            <h5><a>{author}</a></h5>
                            <p>{timestamp}</p>
                        </div>
                        <div class="comment-body">
                            <p>{text}</p>
                            <a class="reply" data-id="{id}" data-parent="{parent_id}">Ответить</a>
                            <form action="" method="POST" class="comment-form form-group" id="form-{id}" style="display:none;">
                                <div class="comment" style="display:block;">
                                    <textarea type="text" class="form-control" name="comment-text"></textarea></br>
                                </div>    
                                <div class="post" style="position:relative">
                                    <input type="submit" class="submit-reply" data-id="{id}" 
                                            data-submit-reply="{parent_id}" value="Отправить">
                                </div>       
                            </form> 
                        </div>
                     </section>
                </article>
             </li>                              
             """.format(id=comment['id'], parent_id=comment['parent_id'], timestamp=comment['timestamp'],
                        text=comment['text'], author=comment['author']
                        )
        if comment.get('children'):
            i += comments_filter(comment.get('children'))
    return mark_safe(res.format(i))