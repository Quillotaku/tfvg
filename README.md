# tfvg
Generates all variables from your .tf files into a variables.tf file.
It searches for every var.variable_name in your .tf files and generates a variables.tf file with the following for every variable:

```hcl
variable "variable_name" {
    type = 
    description = ""
    default = ""
}
```

It's safe to use even if you already have a variable.tf file, it will just add the ones that are not present.


# USE
Just execute this script on the path of your .tf files where you want to generate your variables.tf file. If your are working in a module, then you execute it on the module path, if you are on the main directory of the terraform folder, then there.
