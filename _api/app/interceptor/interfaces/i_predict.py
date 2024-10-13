class IPredict:
    def __init__(self, data):
        self.date  = data.DateField(max_length=11, blank=False, unique=True, primary_key=True) #data.DateTimeField(auto_now_add=True)
        self.PRECTOTCORR  = data.DecimalField(max_digits=10, decimal_places=2, null=True)
        self.RH2M = data.DecimalField(max_digits=10, decimal_places=2, null=True)
        self.QV2M = data.DecimalField(max_digits=10, decimal_places=2, null=True)
        self.T2M = data.DecimalField(max_digits=10, decimal_places=2, null=True)
        self.WS2M = data.DecimalField(max_digits=10, decimal_places=2, null=True)
