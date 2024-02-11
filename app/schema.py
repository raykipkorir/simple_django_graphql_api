import graphene
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType

from .models import Author, Post


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = "__all__"


class Query(graphene.ObjectType):
    authors = graphene.List(AuthorType)
    posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int(required=True))

    def resolve_authors(self, info):
        return Author.objects.all()

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_post(self, info, id):
        return Post.objects.get(id=id)


class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.ID(required=True)

    # output field
    post = graphene.Field(PostType)

    def mutate(self, info, title, content, author_id):
        author = Author.objects.get(id=author_id)
        post = Post.objects.create(title=title, content=content, author=author)

        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)

    def mutate(self, info, id, title=None, content=None):
        post = get_object_or_404(Post, id=id)

        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        post.save()
        return UpdatePost(post=post)


class DeletePost(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return DeletePost(success=True)


class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
