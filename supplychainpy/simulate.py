from multiprocessing.pool import ThreadPool
from decimal import Decimal
from supplychainpy import model_inventory
from supplychainpy.simulations import monte_carlo
from supplychainpy.simulations.simulation_frame_summary import MonteCarloFrameSummary
from supplychainpy.simulations.monte_carlo_frame import BuildFrame
import pyximport

pyximport.install()
from supplychainpy.simulations.sim_summary import summarize_monte_carlo, frame


def run_monte_carlo_mt(file_path: str, z_value: Decimal, runs: int, reorder_cost: Decimal,
                       file_type: str, period_length: int = 12) -> list:
    pool = ThreadPool(processes=4, )
    async_results = pool.apply_async(run_monte_carlo,
                                     (file_path, z_value, runs, reorder_cost, file_type, period_length,))

    return_val = async_results.get()

    return return_val


def run(simulation_frame: list, period_length: int = 12):
    pool = ThreadPool(processes=4, )
    async_results = pool.apply_async(summarize_window, (simulation_frame, period_length,))

    return_val = async_results.get()

    return return_val


def run_monte_carlo(file_path: str, z_value: Decimal, runs: int, reorder_cost: Decimal,
                    file_type: str, period_length: int = 12) -> list:
    """Runs monte carlo simulation.

    Generates random distribution for demand over period specified and creates a simulation window for opening_stock,
    demand, closing_stock, delivery and backlog for each sku in the data set. Creates a transaction summary window
    for inventory movements.

    Args:
        file_path (str):        The path to the file containing two columns of data, 1 period and 1 data-point per sku.
        reorder_cost (Decimal): The average lead-time for the sku over the period represented by the data,
                                in the same unit.
        period_length (int):    The number of periods define the simulation window e.g. 12 weeks, months etc.
        reorder_cost (Decimal): The cost to place a reorder. This is usually the cost of the operation divided
                                by number.
        z_value (Decimal):      The service level required to calculate the safety stock
        file_type (str):        Type of 'file csv' or 'text'
        runs (int):             The number of times to run the simulation.

    Returns:
        list:       A list containing the transaction summary for each period.
                    [[{'closing_stock': '0', 'backlog': '240', 'po_quantity': '6009', 'po_raised': 'PO 49', 'revenue':
                    '1145799', 'opening_stock': '1700', 'index': '9', 'period': '1', 'shortage_units': '240.4612',
                    'po_received': '', 'delivery': '0', 'shortage_cost': '48621', 'demand': '1940',
                    'quantity_sold': '1699', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '240', 'backlog': '852', 'po_quantity': '6380', 'po_raised':
                    'PO 59', 'revenue': '0', 'opening_stock': '0', 'index': '9', 'period': '2',
                    'shortage_units': '611.5989', 'po_received': '', 'delivery': '0', 'shortage_cost': '123665',
                    'demand': '612', 'quantity_sold': '0', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '0', 'backlog': '383', 'po_quantity': '6152', 'po_raised':
                    'PO 69', 'revenue': '162070', 'opening_stock': '240', 'index': '9', 'period': '3',
                    'shortage_units': '383.4993', 'po_received': '', 'delivery': '0', 'shortage_cost': '77543',
                    'demand': '624', 'quantity_sold': '240', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '4463', 'backlog': '383', 'po_quantity': '1689', 'po_raised': 'PO 79',
                    'revenue': '2749508', 'opening_stock': '0', 'index': '9', 'period': '4',
                    'shortage_units': '0.000000', 'po_received': 'PO 49', 'delivery': '6010',
                    'shortage_cost': '0', 'demand': '1547', 'quantity_sold': '4079', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '8002', 'backlog': '0', 'po_quantity': '0', 'po_raised': '',
                    'revenue': '5393458', 'opening_stock': '4463', 'index': '9', 'period': '5',
                    'shortage_units': '0.000000', 'po_received': 'PO 59', 'delivery': '6381',
                    'shortage_cost': '0', 'demand': '2841', 'quantity_sold': '8002', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '13594', 'backlog': '0', 'po_quantity': '0', 'po_raised': '',
                    'revenue': '9162457', 'opening_stock': '8002', 'index': '9', 'period': '6',
                    'shortage_units': '0.000000', 'po_received': 'PO 69', 'delivery': '6153',
                    'shortage_cost': '0', 'demand': '561', 'quantity_sold': '13594', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '13144', 'backlog': '0', 'po_quantity': '0', 'po_raised': '',
                    'revenue': '8859056', 'opening_stock': '13594', 'index': '9', 'period': '7',
                    'shortage_units': '0.000000', 'po_received': 'PO 79', 'delivery': '1690',
                    'shortage_cost': '0', 'demand': '2140', 'quantity_sold': '13144', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '11666', 'backlog': '0', 'po_quantity': '0', 'po_raised': '',
                    'revenue': '7862688', 'opening_stock': '13144', 'index': '9', 'period': '8',
                    'shortage_units': '0.000000', 'po_received': '', 'delivery': '0', 'shortage_cost': '0',
                    'demand': '1478', 'quantity_sold': '11665', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '8542', 'backlog': '0', 'po_quantity': '0', 'po_raised': '',
                    'revenue': '5757540', 'opening_stock': '11666', 'index': '9', 'period': '9',
                    'shortage_units': '0.000000', 'po_received': '', 'delivery': '0', 'shortage_cost': '0',
                    'demand': '3123', 'quantity_sold': '8542', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '7832', 'backlog': '0', 'po_quantity': '0', 'po_raised': '',
                    'revenue': '5278665', 'opening_stock': '8542', 'index': '9', 'period': '10',
                    'shortage_units': '0.000000', 'po_received': '', 'delivery': '0', 'shortage_cost': '0',
                    'demand': '710', 'quantity_sold': '7831', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '5379', 'backlog': '0', 'po_quantity': '389', 'po_raised': 'PO 149',
                    'revenue': '3625634', 'opening_stock': '7832', 'index': '9', 'period': '11', 'shortage_units':
                    '0.000000', 'po_received': '', 'delivery': '0', 'shortage_cost': '0', 'demand': '2453',
                    'quantity_sold': '5379', 'sku_id': 'KR202-217'}]
                    [{'closing_stock': '3799', 'backlog': '0', 'po_quantity': '1969', 'po_raised': 'PO 159',
                    'revenue': '2560610', 'opening_stock': '5379', 'index': '9', 'period': '12',
                    'shortage_units': '0.000000', 'po_received': '', 'delivery': '0', 'shortage_cost': '0',
                    'demand': '1580', 'quantity_sold': '3799', 'sku_id': 'KR202-217'}],...]

    """

    orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=file_path,
                                                                      z_value=z_value,
                                                                      reorder_cost=reorder_cost,
                                                                      file_type=file_type)
    Transaction_report = []
    # add shortage cost,
    for k in range(0, runs):
        simulation = monte_carlo.SetupMonteCarlo(analysed_orders=orders_analysis.orders)
        random_demand = simulation.generate_normal_random_distribution(period_length=period_length)
        for sim_window in simulation.build_window(random_normal_demand=random_demand, period_length=period_length):
            sim_dict = {"index": "{}".format(sim_window.index), "period": "{}".format(sim_window.position),
                        "sku_id": sim_window.sku_id, "opening_stock": "{}".format(round(sim_window.opening_stock)),
                        "demand": "{}".format(round(sim_window.demand)),
                        "closing_stock": "{}".format(round(sim_window.closing_stock)),
                        "delivery": "{}".format(round(sim_window.purchase_order_receipt_qty)),
                        "backlog": "{:.0f}".format(sim_window.backlog),
                        "po_raised": "{}".format(sim_window.po_number_raised),
                        "po_received": "{}".format(sim_window.po_number_received),
                        "po_quantity": "{:.0f}".format(int(sim_window.purchase_order_raised_qty)),
                        "shortage_cost": "{:.0f}".format(Decimal(sim_window.shortage_cost)),
                        "revenue": "{:.0f}".format(sim_window.revenue),
                        "quantity_sold": "{:0.0f}".format(sim_window.sold),
                        "shortage_units": "{:.0f}".format(sim_window.shortage_units)}
            # so = BuildFrame(s=sim_dict)
            Transaction_report.append([sim_dict])
    return Transaction_report


def summarize_window(simulation_frame: list, period_length: int = 12):
    """ Summarizes the simulation window and provides the stockout percentage for each sku.

    Provides a summary of inventory transactions, for the full period length for each run.

    Args:
       simulation_frame (list):     A collection of simulation windows.
       period_length (int):         The number of periods define the simulation window e.g. 12 weeks, months etc.

    Returns:
       list:    A list containing the results for each sku.[{'maximum_opening_stock': 13181.0,
                'standard_deviation_closing_stock': 4407.468727436796, 'standard_deviation_backlog': 485.2568835735928,
                'variance_backlog': 235474.24305555542, 'minimum_backlog': 0.0, 'maximum_closing_stock': 13181.0,
                'standard_deviation_shortage_cost': 348.8327422580442, 'variance_opening_stock': 20387450.520833332,
                'average_opening_stock': 6350.75, 'minimum_quantity_sold': 0.0,
                'standard_deviation_opening_stock': 4515.246451837744, 'stockout_percentage': 0.0833333358168602,
                'maximum_backlog': 1337.0, 'sku_id': 'KR202-240', 'standard_deviation_revenue': 4489.574661244527,
                'maximum_quantity_sold': 13181.0, 'total_quantity_sold': 76742.0,
                'variance_quantity_sold': 20156280.638888914, 'minimum_closing_stock': 0.0,
                'variance_closing_stock': 19425780.583333332, 'variance_shortage_units': 121684.28207126712,
                'index': '32', 'average_closing_stock': 6461.5, 'total_shortage_units': 1337.80962,
                'maximum_shortage_units': 1266.604, 'minimum_shortage_units': 0.0, 'average_backlog': 216.9166717529297,
                'minimum_opening_stock': 0.0}...]
    """

    summary = summarize_monte_carlo(simulation_frame, period_length)

    return summary


def summarise_frame(window_summary):
    """ Summarizes the simulation frame
    Generates a summary for run window, into 1 transaction summary for all the runs.

    Args:
        window_summary  (list): window summary for each period multiplied by the number of runs.

    Returns:
       list:    [{'variance_opening_stock': '5007', 'maximum_opening_stock': 13805, 'maximum_backlog': 2278.0,
                'minimum_quantity_sold': 0.0, 'average_backlog': '218', 'minimum_opening_stock': 0,
                'average_quantity_sold': '7204', 'maximum_quantity_sold': 13805.0, 'minimum_closing_stock': 0,
                'standard_deviation_backlog': '628', 'standard_deviation_quantity_sold': '4636',
                'maximum_closing_stock': 13805, 'standard_deviation_closing_stock': '4755',
                'average_shortage_units': '2278', 'service_level': '91.67','minimum_backlog': 0.0,
                'average_closing_stock': '7115', 'sku_id': 'KR202-240'},...]

    """

    frame_summary = frame(window_summary)
    return frame_summary
