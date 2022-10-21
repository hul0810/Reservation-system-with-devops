# import graphene
# from schemas import building_gql
# from database import db_session
# from models import Building

# class Query(graphene.ObjectType):
#     read_all = graphene.List(building_gql)

#     def resolve_read_all(self, info):
#         query = building_gql.get_query(info)
#         return query.all() # 에러 발생(세션 close 해주는 로직 구현해줘야 하는듯)


    # def resolve_read_all(self, info):
    #     return db.query(Building).all()

    # def resolve_post_by_id(self, info, bid):
    #     return db.query(Building).filter(Building.bid == bid).first()