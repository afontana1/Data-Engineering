def enrich_features(tensors: List[Tensor], keys: List[str], args: List[str]):
    features = args
    credit_features = [str(x) for x in redis.asList(redis.execute("HVALS", keys[0]))]
    zipcode_features = [str(x) for x in redis.asList(redis.execute("HVALS", keys[1]))]
    features.extend(credit_features)
    features.extend(zipcode_features)
    input_tensor = torch.tensor([float(feature) for feature in features]).reshape(1, 17)
    return input_tensor
