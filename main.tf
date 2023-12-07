# The configuration for the `remote` backend.
terraform {
  backend "remote" {
    organization = "example-organization"

    workspaces {
      name = "example-workspace"
    }
  }
}

# An example resource that does nothing.
resource "null_resource" "example" {
  triggers = {
    value = "A example resource that does nothing!"
  }
}
