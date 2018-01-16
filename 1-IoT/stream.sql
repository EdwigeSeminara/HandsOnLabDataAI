WITH anomaly AS (
    SELECT cast(T as float) as T,
    cast(V as float) as V,
    cast(AP as float) as AP,
    cast(RH as float) as RH,
    cast(PE as float) as PE,
    cast(anomaly(T, V, AP, RH, PE) as float) as result
    from holBlobIn
)

Select System.Timestamp as date, T, V, AP, RH, PE, result

Into holBlobOut

From anomaly

Select System.Timestamp as date,T, V, AP, RH, PE, result

Into holPbiOut

From anomaly