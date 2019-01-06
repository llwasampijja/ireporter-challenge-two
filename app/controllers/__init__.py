# def delete_incident(self, incident_id, keyword, username):
#         delete_incident_instance = incident_data.delete_incident(
#             incident_id, keyword, username)
#         if delete_incident_instance is None:
#             return self.response_unaccepted("none")
#         elif delete_incident_instance == "non_author":
#             return Response(json.dumps({
#                 "status": 401,
#                 "message": RESP_UNAUTHORIZED_DELETE
#             }), content_type="application/json", status=401)
#         else:
#             return self.response_sumission_success(delete_incident_instance,
#                                                    "delete")


#     if update_incident_instance is None:
#             return self.response_unaccepted("none")
#         elif update_incident_instance == "non_author":
#             return Response(json.dumps({
#                 "status": 401,
#                 "message": RESP_UNAUTHORIZED_EDIT
#             }), content_type="application/json", status=401)
#         else:
#             return self.response_sumission_success(update_incident_instance,
#                                                    "update")
# def delete_update(action_instance, message_fail, message_success):
#     if action_instance is None:
#             return self.response_unaccepted("none")
#         elif action_instance == "non_author":
#             return Response(json.dumps({
#                 "status": 401,
#                 "message": message_fail
#             }), content_type="application/json", status=401)
#         else:
#             return message_success
