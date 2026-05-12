from tools.order_lookup import order_lookup
from tools.customer_profile import customer_profile
from tools.refund_tool import request_refund
from tools.complaint_logger import log_complaint

print("=== order_lookup（normal）===")
print(order_lookup(1001))

print("\n=== customer_profile ===")
print(customer_profile(1))

print("\n=== request_refund（delivered:should success）===")
print(request_refund(7890))

print("\n=== request_refund（shipped:should fail）===")
print(request_refund(2222))

print("\n=== log_complaint ===")
print(log_complaint(2, 2222, "Package arrived damaged"))

print("\n=== order_lookup（not found）===")
print(order_lookup(9999))
