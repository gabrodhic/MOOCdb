class UploadsController < ApplicationController

  def home

  end

  def index
  end

  def new
    @upload = Upload.new
  end

  def create
    @upload = Upload.new(params[:upload])
    @upload.save
    redirect_to root_path
  end
end
