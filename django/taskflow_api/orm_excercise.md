>>> ProjectTaxi.objects.all()
<QuerySet [<ProjectTaxi: Amarilla>, <ProjectTaxi: Azul>]>
>>> ProjectTaxi.objects.create(taxi="Rosa",taxi_placa="PPP 2223",taxi_chofer="Mar nandez",taxi_tarifa="31$")
<ProjectTaxi: Rosa>
>>> ProjectTaxi.objects.all()
<QuerySet [<ProjectTaxi: Amarilla>, <ProjectTaxi: Azul>, <ProjectTaxi: Rosa>]>
>>> 