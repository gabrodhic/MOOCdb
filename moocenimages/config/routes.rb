Moocenimages::Application.routes.draw do
  root :to => "visualizations#index"

  resources :users
  resources :user_sessions
end
