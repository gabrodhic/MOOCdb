class VisualizationsController < ApplicationController

  def home

  end

  def index
  end

  def get_file
    name = params[:name]
    viz = Visualization.find(:id => 5)
    @file = viz.content

    respond_to do |format|
        format.json { render json: @file }
    end
  end
end
