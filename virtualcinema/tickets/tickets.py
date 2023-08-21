from datetime import datetime

from flask import Blueprint, request
from virtualcinema.auth import auth
from virtualcinema.models.models import ModelAccount, ModelTickets, ModelSeat

tickets = Blueprint('tickets', __name__)


@tickets.route('/tickets', methods=['GET'])
@auth
def handler_get_ticket():
    session = ModelAccount.query.filter_by(u_username=request.authorization.username).first()
    query = ModelTickets.query.filter_by(id_user=session.id_user).all()

    if session.u_role == 'Admin':
        query = ModelTickets.query.all()
    if not query:
        return {"Error": "Tickets not found"}, 404

    currentdate = datetime.now().strftime("%d-%m-%Y")
    currenttime = datetime.now().strftime("%H:%M")

    response = [{
        "id_ticket": row.id_ticket,
        "film_name": row.orders.schedules.film.film_name,
        "order_seat": [ModelSeat.query.filter_by(id_seat=seat.id_seat).first().seat_number for seat in row.orders.orderseat],
        "order_studio": row.orders.order_studio,
        "order_date": row.orders.order_date,
        "order_time": row.orders.order_time,
        "ticket_status": "Active" if currentdate == row.orders.order_date and currenttime <= row.orders.order_time or currentdate < row.orders.order_date else "Expired",
    } for row in query]
    return {"Message": "Success", "Count": len(response), "Data": response}, 200
