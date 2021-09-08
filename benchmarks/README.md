# Benchmarks

We have chose two suites of benchmarks to use for evaluation. The first, spec2017 will be familiar to architects. The latter, the ECP Proxy App suite serves our goal attempting to 

## Spec2017

Spec is not free software, so you must obtain a copy yourself. Once you have that, you can place our config file, `morrigan.cfg` in your spec config folder, $SPEC/config, and run the following commands:

```
specrun --action=build --config=morrigan specspeed
```

## ECP Proxy Apps

We use the ECP Proxy Apps to exten our analysis to programs of interest to the HPC community. These can be installed with Spack. You can  either let Spack  

### Simple Install

If you do not care about using the exact same versions of every package as we did, simply execute the following command:

```
spack install ecp-proxy-apps ^openmpi@3:3.9
```

### 

To use the same versions of all the software as us
