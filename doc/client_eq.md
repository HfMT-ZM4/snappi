# Implement EQ or other filter effects on client

You can use LADSPA effects on the Snappi client to implement
EQ or other filters. You need to create an /etc/asound.conf file
with filter effect definitions. Some examples:

# Only high-pass and low-pass filters

This example uses the simple HPF and LPF LADSPA filters from the
example plugins: ttps://www.ladspa.org/ladspa_sdk/example_plugins.html.

/etc/asound.conf
```
pcm.effects {
    type ladspa
    slave.pcm "plughw:0,0"
    path "/usr/lib/ladspa"
    plugins [
        {
            label "lpf"
            policy none
            input.bindings.0 "Input";
            output.bindings.0 "Output";
            input {
                controls [ 440.0 ]
            }
        }
        {
            label "hpf"
            policy none
            input.bindings.1 "Input";
            output.bindings.1 "Output";
            input {
                controls [ 440.0 ]
            }
        }
    ]
}

pcm.!default {
    type plug;
    slave.pcm "effects";
}
```

# High-pass and low-pass with EQ

This example uses the HPF and LPF filters from the example plugins and also
the Eq4p filter from the CAPS library: http://quitte.de/dsp/caps.html#Eq4p

/etc/asound.conf
```
pcm.effects {
    type ladspa
    slave.pcm "plughw:0,0"
    path "/usr/lib/ladspa"
    plugins [
        {
            label "hpf"
            policy none
            input.bindings.0 "Input";
            output.bindings.0 "Output";
            input {
                controls [ 440.0 ]
            }
        }
        {
            label "lpf"
            policy none
            input.bindings.1 "Input";
            output.bindings.1 "Output";
            input {
                controls [ 440.0 ]
            }
        }
        {                                                                                                                                                                                  
            label "Eq4p"                                                                                                                                                                   
            policy "none"                                                                                                                                                                  
            input.bindings.0 "in"                                                                                                                                                          
            output.bindings.0 "out"                                                                                                                                                        
            input.controls {                                                                                                                                                               
              "a.mode" 0                                                                                                                                                                   
              "a.f (Hz)" 440                                                                                                                                                               
              "a.Q" 0                                                                                                                                                                      
              "a.gain (dB)" -48                                                                                                                                                            
            }                                                                                                                                                                              
        }                                                                                                                                                                                  
        {                                                                                                                                                                                  
            label "Eq4p"                                                                                                                                                                   
            policy "none"                                                                                                                                                                  
            input.bindings.1 "in"                                                                                                                                                          
            output.bindings.1 "out"                                                                                                                                                        
            input.controls {                                                                                                                                                               
              "d.mode" 2                                                                                                                                                                   
              "d.f (Hz)" 2440                                                                                                                                                              
              "d.Q" 0                                                                                                                                                                      
              "d.gain (dB)" -48                                                                                                                                                            
            }                                                                                                                                                                              
        }                                                                                                                                                                                  
    ]
}

pcm.!default {
    type plug;
    slave.pcm "effects";
}
```
