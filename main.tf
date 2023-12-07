# The configuration for the `remote` backend.
terraform {
  cloud {
    organization = "C4_Final_Proj"

    workspaces {
      name = "c4-final-proj"
    }
  }
}

#
#     # An example resource that does nothing.
resource "null_resource" "example" {
  triggers = {
    value = "A example resource that does nothing!"
  }
}
