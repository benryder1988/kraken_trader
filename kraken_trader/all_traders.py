import numpy as np


class standard_trader():

    def __init__(self,conn,k):
        self.conn = conn
        self.k = k

    def get_buy_advice(self):

        return (0,1)

    def get_sell_advice(self):

        return (0,1)

class basic_trader():
    """
    Returns the most increasing FX to buy and the most decreasing to sell
    """

    def __init__(self,conn,k,pairs):
        self.conn = conn
        self.k = k
        self.pairs = pairs
        self.pred = dict()
        self.diff = dict()

        #Calculate the predicted change
        self.predict_change(0.5)

    def get_buy_advice(self,time):

        ask_list_pred = dict()
        for key in self.pred:
            # TODO: check if time is not larger
            elem = np.argmin(np.abs(np.matrix(self.pred.get(key))[:,0]-time))
            ask_list_pred.update({key:self.pred.get(key)[elem][1]})
        return (max(ask_list_pred,key=ask_list_pred.get),1)

    def get_sell_advice(self,time):

        bid_list_pred = dict()
        for key in self.pred:
            # TODO: check if time is not larger
            elem = np.argmin(np.abs(np.matrix(self.pred.get(key))[:,0]-time))
            bid_list_pred.update({key:self.pred.get(key)[elem][2]})
        return (min(bid_list_pred, key=bid_list_pred.get),1)

    def predict_change(self,alpha):

        for pair in self.pairs:
            cur = self.conn.cursor()
            cur.execute("SELECT modtime, ask_price, bid_price FROM "+ pair)
            res = cur.fetchall()
            cur.close()

            #TODO: put here the filter, strategy or whatever
            self.pred[pair] = []
            self.pred[pair].append(np.array(res[0]))
            for i in range(1,len(res)):
                pred_val = np.add(alpha*np.array(res[i][1:]), (1-alpha)*np.array(self.pred[pair][-1][1:]))
                abs_change = np.subtract(pred_val,res[i][1:])
                #TODO: check if correct this way...
                self.pred[pair].append(np.insert(res[i][0],1,np.divide(abs_change,res[i][1:])))