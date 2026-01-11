resource "kubernetes_service" "iris-api" {
  metadata {
    name      = "${var.app_name}-service"
    namespace = var.namespace
    labels = {
      app = var.app_name
    }
  }

  spec {
    type = "LoadBalancer"

    selector = {
      app = var.app_name
    }

    port {
      name        = "http"
      port        = 80
      target_port = 8000
      protocol    = "TCP"
    }
  }
}
